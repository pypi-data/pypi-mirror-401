"""Async HTTP client for SynthWell Prototype backend."""

import logging
from functools import lru_cache
from typing import Any

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

# Default timeouts
DEFAULT_TIMEOUT = 30.0  # 30 seconds for most endpoints
CHAT_TIMEOUT = 120.0  # 2 minutes for chat (Claude API can be slow with RAG)
ANALYZE_TIMEOUT = 180.0  # 3 minutes for analyze (long-running)


class SynthWellClientError(Exception):
    """Error from SynthWell API."""

    def __init__(self, message: str, status_code: int | None = None, response: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class SynthWellClient:
    """
    Async HTTP client for SynthWell Prototype backend.

    Provides methods for:
    - Chat interactions (fast mode)
    - Journey creation and updates
    - Persona simulation
    - Analysis jobs
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        settings = get_settings()
        self.base_url = (base_url or settings.synthwell_api_url).rstrip("/")
        self.api_key = api_key or settings.synthwell_api_key
        self.timeout = timeout

        # Build headers
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            self.headers["X-API-Key"] = self.api_key

    def _get_client(self, timeout: float | None = None) -> httpx.AsyncClient:
        """Create an async HTTP client with configured settings."""
        # Use explicit timeout config for better control over connection phases
        timeout_config = httpx.Timeout(
            timeout=timeout or self.timeout,
            connect=30.0,  # Connection timeout
        )
        return httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=timeout_config,
            http2=False,  # Disable HTTP/2 for better Railway compatibility
        )

    async def _request(
        self,
        method: str,
        path: str,
        timeout: float | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """Make an HTTP request and handle errors."""
        async with self._get_client(timeout) as client:
            try:
                response = await client.request(method, path, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                error_body = None
                try:
                    error_body = e.response.json()
                except Exception:
                    pass
                logger.error(
                    f"SynthWell API error: {e.response.status_code} - {error_body or e.response.text}"
                )
                raise SynthWellClientError(
                    f"API error: {e.response.status_code}",
                    status_code=e.response.status_code,
                    response=error_body,
                )
            except httpx.TimeoutException:
                logger.error(f"SynthWell API timeout on {method} {path}")
                raise SynthWellClientError("Request timed out")
            except httpx.RequestError as e:
                logger.error(f"SynthWell API request error on {method} {path}: {type(e).__name__}: {e}")
                raise SynthWellClientError(f"Request failed: {type(e).__name__}: {str(e)}")

    # ==========================================
    # Chat Endpoints
    # ==========================================

    async def chat_fast(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Send a message to the fast chat endpoint.

        Args:
            message: User message content
            conversation_id: Optional conversation ID for continuity

        Returns:
            Chat response with assistant message and metadata
        """
        payload = {"message": message}
        if conversation_id:
            payload["conversation_id"] = conversation_id

        return await self._request("POST", "/chat/fast", json=payload, timeout=CHAT_TIMEOUT)

    # ==========================================
    # Journey Endpoints
    # ==========================================

    async def create_journey(
        self,
        zip_codes: list[str],
        name: str | None = None,
        plan_type: str | None = None,
        campaign_type: str = "aep_acquisition",
        user_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a new journey with cohort parameters.

        Args:
            zip_codes: List of target ZIP codes
            name: Journey name (auto-generated if not provided)
            plan_type: Optional plan type filter (e.g., "MA", "PDP")
            campaign_type: Campaign type (default: "aep_acquisition")
            user_id: Optional user ID for journey ownership

        Returns:
            Created journey with ID and initial configuration
        """
        payload: dict[str, Any] = {
            "name": name or f"Journey for {', '.join(zip_codes[:3])}",
            "zip_codes": zip_codes,
            "campaign_type": campaign_type,
        }
        if plan_type:
            payload["plan_type"] = plan_type
        if user_id:
            payload["user_id"] = user_id

        return await self._request("POST", "/journey/create", json=payload, timeout=CHAT_TIMEOUT)

    async def create_flowchart_v2(
        self,
        zip_codes: list[str],
        campaign_type: str = "aep_acquisition",
        name: str | None = None,
        user_id: str | None = None,
        created_from: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a journey using the full v2 pipeline with grounded architecture.

        This is the full pipeline that includes:
        - 15+ data source ingestion (Census, CDC, CMS, etc.)
        - Synthetic cohort generation (5,000 personas)
        - Monte Carlo simulation
        - Claude Opus 4.5 strategic reasoning
        - "Because" layer with data citations

        Takes ~80-120 seconds to complete.

        Args:
            zip_codes: List of target ZIP codes (1-10)
            campaign_type: Campaign type (e.g., 'aep_acquisition', 'turning_65')
            name: Optional journey name
            user_id: Optional user ID for journey ownership
            created_from: Optional source identifier (e.g., 'cli', 'web')

        Returns:
            Full flowchart response with nodes, edges, market_profile, terry_insights
        """
        payload: dict[str, Any] = {
            "zip_codes": zip_codes,
            "campaign_type": campaign_type,
        }
        if name:
            payload["name"] = name
        if user_id:
            payload["user_id"] = user_id
        if created_from:
            payload["created_from"] = created_from

        # Full pipeline takes 80-120s
        return await self._request(
            "POST",
            "/journey/flowchart/create-v2",
            json=payload,
            timeout=ANALYZE_TIMEOUT,  # 3 minutes
        )

    async def get_journey(self, journey_id: str) -> dict[str, Any]:
        """Get journey by ID."""
        return await self._request("GET", f"/journey/{journey_id}")

    async def update_journey(
        self,
        journey_id: str,
        touchpoints: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Update journey touchpoints.

        Args:
            journey_id: Journey ID to update
            touchpoints: List of touchpoint configurations

        Returns:
            Updated journey data
        """
        payload = {
            "journey_id": journey_id,
            "touchpoints": touchpoints,
        }
        return await self._request("POST", "/journey/update", json=payload)

    # ==========================================
    # Simulation Endpoints
    # ==========================================

    async def simulate_personas(
        self,
        message: dict[str, Any],
        cohort_filters: dict[str, Any] | None = None,
        sample_size: int = 100,
    ) -> dict[str, Any]:
        """
        Run persona simulation on a cohort (legacy endpoint).

        Args:
            message: Message/journey configuration to simulate
            cohort_filters: Optional filters for cohort selection
            sample_size: Number of synthetic personas to simulate

        Returns:
            Simulation results with persona responses and aggregated metrics
        """
        payload = {
            "message": message,
            "sample_size": sample_size,
        }
        if cohort_filters:
            payload["cohort_filters"] = cohort_filters

        return await self._request(
            "POST",
            "/personas/simulate",
            json=payload,
            timeout=ANALYZE_TIMEOUT,  # Simulation can take time
        )

    async def simulate_journey(
        self,
        journey_id: str,
        baseline_touchpoints: list[dict[str, Any]],
        modified_touchpoints: list[dict[str, Any]],
        cohort_profile: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Simulate the impact of journey changes using the physics engine.

        Compares baseline touchpoints against modified touchpoints to show
        the impact of proposed changes (e.g., "what if we add a mailer?").

        Args:
            journey_id: Journey ID (used to load stored cohort profile if not provided)
            baseline_touchpoints: Current journey state (list of touchpoint dicts with
                channel, day, stage fields)
            modified_touchpoints: Proposed changes (same structure as baseline)
            cohort_profile: Optional cohort behavioral profile override with:
                - effort_tolerance_score (0-1)
                - confusion_susceptibility (0-1)
                - institutional_trust_score (0-1)
                - digital_channel_score (0-1)

        Returns:
            Simulation results with:
            - baseline: SimulationOutput (advance_probability, dropout_probability, etc.)
            - modified: SimulationOutput
            - delta: Changes between baseline and modified with interpretation
        """
        payload: dict[str, Any] = {
            "baseline_touchpoints": baseline_touchpoints,
            "modified_touchpoints": modified_touchpoints,
        }

        if cohort_profile:
            payload["cohort_profile"] = cohort_profile

        # Debug logging
        logger.info(f"simulate_journey: POST {self.base_url}/journey/{journey_id}/simulate")
        logger.info(f"simulate_journey payload: baseline={len(baseline_touchpoints)} touchpoints, modified={len(modified_touchpoints)} touchpoints")

        return await self._request(
            "POST",
            f"/journey/{journey_id}/simulate",
            json=payload,
            timeout=ANALYZE_TIMEOUT,  # Simulation can take time
        )

    async def optimize_journey(
        self,
        touchpoints: list[dict[str, Any]],
        simulation_results: dict[str, Any] | None = None,
        target_conversion: float = 0.15,
        max_iterations: int = 3,
    ) -> dict[str, Any]:
        """
        Optimize a journey to improve conversion rate.

        Analyzes the journey for issues (low engagement, dropoffs, fatigue) and
        suggests/applies refinements.

        Args:
            touchpoints: Current journey touchpoints (list of dicts with id, channel, day)
            simulation_results: Optional simulation results with stage_predictions
            target_conversion: Target conversion rate (default 15%)
            max_iterations: Maximum optimization iterations (default 3)

        Returns:
            Optimization results with:
            - success: Whether target was met
            - original_conversion: Starting conversion rate
            - optimized_conversion: Ending conversion rate
            - improvement: Percentage points improvement
            - optimized_touchpoints: Refined touchpoints if successful
            - versions: History of optimization iterations
            - recommendations: Human-readable suggestions
        """
        payload: dict[str, Any] = {
            "touchpoints": touchpoints,
            "target_conversion": target_conversion,
            "max_iterations": max_iterations,
        }

        if simulation_results:
            payload["simulation_results"] = simulation_results

        return await self._request(
            "POST",
            "/journey/optimize",
            json=payload,
            timeout=ANALYZE_TIMEOUT,  # Optimization can take time
        )

    # ==========================================
    # Analysis Endpoints
    # ==========================================

    async def analyze(
        self,
        message: str,
        deliverables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Start an analysis job.

        Args:
            message: Analysis request/query
            deliverables: Optional deliverable specifications

        Returns:
            Job ID and initial status
        """
        payload = {"message": message}
        if deliverables:
            payload["deliverables"] = deliverables

        return await self._request(
            "POST",
            "/analyze",
            json=payload,
            timeout=ANALYZE_TIMEOUT,
        )

    async def get_analyze_status(self, job_id: str) -> dict[str, Any]:
        """
        Get status of an analysis job.

        Args:
            job_id: Job ID to check

        Returns:
            Job status and results (if complete)
        """
        return await self._request("GET", f"/analyze/{job_id}")

    # ==========================================
    # Location Endpoints
    # ==========================================

    async def location_autocomplete(
        self,
        query: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        """
        Get autocomplete suggestions for a location query.

        Args:
            query: Search query (e.g., "mia", "flor", "north")
            limit: Maximum suggestions to return

        Returns:
            Autocomplete response with suggestions list
        """
        return await self._request(
            "GET",
            "/location/autocomplete",
            params={"q": query, "limit": limit},
        )

    async def analyze_geography(
        self,
        location_type: str,
        location_value: str,
    ) -> dict[str, Any]:
        """
        Analyze a geographic area and return its market clusters.

        For broad geographies (states, regions, national), returns distinct
        market segments that the user should choose from for targeted messaging.

        Args:
            location_type: Type of location (state, region, national, city, zip)
            location_value: Location value (e.g., 'CA', 'northeast', 'national')

        Returns:
            Analysis response with:
            - location_label: Human-readable name
            - total_zips: Number of ZIPs in geography
            - requires_cluster_selection: Whether user should pick a cluster
            - clusters: List of market segments with id, label, description, traits
            - message: Guidance for the user
        """
        return await self._request(
            "GET",
            "/geography/analyze",
            params={"location_type": location_type, "location_value": location_value},
        )

    async def resolve_location(
        self,
        location_type: str,
        location_value: str,
        cluster_id: str | None = None,
        max_zips: int = 10,
    ) -> dict[str, Any]:
        """
        Resolve a location to ZIP codes.

        Args:
            location_type: Type of location (zip, city, state, region, national)
            location_value: Location value (e.g., 'CA', 'Miami|FL', 'northeast')
            cluster_id: Optional cluster ID for targeted resolution
            max_zips: Maximum ZIPs to return (default 10)

        Returns:
            Resolution response with zip_codes list
        """
        payload = {
            "location_type": location_type,
            "location_value": location_value,
            "max_zips": max_zips,
        }
        if cluster_id:
            payload["cluster_id"] = cluster_id

        return await self._request("POST", "/location/resolve", json=payload)

    # ==========================================
    # Health Check
    # ==========================================

    async def health_check(self) -> dict[str, Any]:
        """Check if the SynthWell backend is healthy."""
        return await self._request("GET", "/health", timeout=5.0)


@lru_cache
def get_synthwell_client() -> SynthWellClient:
    """Get cached SynthWell client instance."""
    return SynthWellClient()
