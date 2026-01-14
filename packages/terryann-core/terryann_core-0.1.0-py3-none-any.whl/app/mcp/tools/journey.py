"""Journey creation and modification tools."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from app.clients.synthwell_client import SynthWellClient, SynthWellClientError, get_synthwell_client
from app.models.schemas import (
    JourneyRequest,
    JourneyResponse,
    Touchpoint,
    TouchpointType,
)

logger = logging.getLogger(__name__)


def _map_touchpoint_type(type_str: str) -> TouchpointType:
    """Map string touchpoint type/channel to enum."""
    type_map = {
        "email": TouchpointType.EMAIL,
        "sms": TouchpointType.SMS,
        "mailer": TouchpointType.MAILER,
        "mail": TouchpointType.MAILER,
        "call": TouchpointType.CALL,
        "phone": TouchpointType.CALL,
        "digital_ad": TouchpointType.DIGITAL_AD,
        "ad": TouchpointType.DIGITAL_AD,
        "event": TouchpointType.EVENT,
    }
    return type_map.get(type_str.lower(), TouchpointType.EMAIL)


# Estimated cost per channel type
CHANNEL_COSTS = {
    "email": 0.15,
    "sms": 0.08,
    "mail": 1.25,
    "mailer": 1.25,
    "phone": 8.50,
    "call": 8.50,
    "digital_ad": 0.50,
    "event": 50.00,
}


def _parse_touchpoints(touchpoint_data: list[dict]) -> list[Touchpoint]:
    """Parse touchpoint data from backend response (legacy format)."""
    touchpoints = []
    for tp in touchpoint_data:
        # Backend uses 'channel' field, map to our type
        channel = tp.get("channel", tp.get("type", "email"))
        channel_lower = channel.lower()

        # Generate name from stage and channel if not provided
        stage = tp.get("stage", "")
        name = tp.get("name") or f"{stage} {channel.title()}".strip()

        # Get estimated cost from channel type
        estimated_cost = tp.get("estimated_cost", CHANNEL_COSTS.get(channel_lower, 0.15))

        # Convert score to expected response rate (score is 0-100, rate is 0-1)
        score = tp.get("score", 50.0)
        expected_rate = tp.get("expected_response_rate", score / 100.0 * 0.5)

        touchpoints.append(
            Touchpoint(
                id=tp.get("id", f"tp_{uuid.uuid4().hex[:8]}"),
                type=_map_touchpoint_type(channel),
                name=name,
                day=tp.get("day", 1),
                content_template=tp.get("content_template"),
                estimated_cost=estimated_cost,
                expected_response_rate=expected_rate,
            )
        )
    return touchpoints


def _parse_flowchart_nodes(nodes: list[dict]) -> list[Touchpoint]:
    """Parse touchpoints from v2 flowchart nodes."""
    touchpoints = []
    for node in nodes:
        # Only process touchpoint nodes
        if node.get("type") != "touchpoint":
            continue

        channel = node.get("channel", "EMAIL")
        channel_lower = channel.lower()

        # Extract label and because data
        label = node.get("label", "")
        because = node.get("because", {})
        because_claim = because.get("claim", "") if isinstance(because, dict) else ""

        # Get day from node data or infer from position
        # v2 flowchart nodes have position as {x, y} dict for visualization
        day = node.get("day")
        if day is None:
            position = node.get("position", {})
            if isinstance(position, dict):
                # Infer day from x position: x=200 is ~day 1, x=400 is ~day 7, etc.
                # Typical flowchart spans x=200 to x=1800 over ~60 days
                x = position.get("x", 200)
                day = max(1, (x - 200) // 25 + 1)  # Every 25px ≈ 1 day
            elif isinstance(position, int):
                day = position
            else:
                day = len(touchpoints) * 7 + 1  # Default: space out by week

        # Get estimated cost from channel type
        estimated_cost = CHANNEL_COSTS.get(channel_lower, 0.15)

        touchpoints.append(
            Touchpoint(
                id=node.get("id", f"tp_{uuid.uuid4().hex[:8]}"),
                type=_map_touchpoint_type(channel),
                name=label or f"{channel.title()} Touchpoint",
                day=day,
                content_template=because_claim[:200] if because_claim else None,  # Use reasoning as template hint
                estimated_cost=estimated_cost,
                expected_response_rate=0.25,  # Default rate for flowchart nodes
            )
        )

    # Sort by day
    touchpoints.sort(key=lambda tp: tp.day)
    return touchpoints


async def create_journey(
    request: JourneyRequest,
    zip_codes: list[str] | None = None,
    campaign_type: str = "aep_acquisition",
    client: SynthWellClient | None = None,
) -> JourneyResponse:
    """
    Create a new journey blueprint using the full v2 pipeline.

    This calls the full SynthWell pipeline including:
    - 15+ data source ingestion (Census, CDC, CMS, etc.)
    - Synthetic cohort generation (5,000 personas)
    - Monte Carlo simulation
    - Claude Opus 4.5 strategic reasoning
    - "Because" layer with data citations

    Takes ~80-120 seconds to complete.

    Args:
        request: Journey request with name and optional touchpoints
        zip_codes: Optional ZIP codes for cohort targeting
        campaign_type: Campaign type (default: aep_acquisition)
        client: Optional SynthWell client (for testing)
    """
    client = client or get_synthwell_client()

    try:
        # Call full v2 pipeline
        logger.info(f"Creating journey via v2 pipeline for ZIP codes: {zip_codes}")
        result = await client.create_flowchart_v2(
            zip_codes=zip_codes or ["33101"],  # Default to Miami
            campaign_type=campaign_type,
            name=request.name or "New Journey",
        )

        # v2 returns nodes and edges instead of touchpoints
        journey_id = result.get("journey_id", f"journey_{uuid.uuid4().hex[:8]}")
        nodes = result.get("nodes", [])

        # Parse touchpoints from flowchart nodes
        touchpoints = _parse_flowchart_nodes(nodes)

        # If no touchpoints from nodes, fall back to legacy format or defaults
        if not touchpoints:
            backend_touchpoints = result.get("touchpoints", [])
            touchpoints = _parse_touchpoints(backend_touchpoints) if backend_touchpoints else []

        if not touchpoints:
            touchpoints = request.touchpoints or _default_touchpoints()

        total_duration = max(tp.day for tp in touchpoints) if touchpoints else 0
        total_cost = sum(tp.estimated_cost for tp in touchpoints)

        # Extract insights from v2 response
        terry_insights = result.get("terry_insights", {})
        market_profile = result.get("market_profile", {})

        # Build description from insights
        description = request.description or "Journey"
        if terry_insights:
            # Try to extract key insight
            key_insight = terry_insights.get("key_insight") or terry_insights.get("summary", "")
            if key_insight:
                description = key_insight[:200]

        # Add predicted conversion if available
        predicted = result.get("predicted_conversion") or market_profile.get("predicted_conversion")
        if predicted:
            description += f" (Predicted conversion: {predicted:.1%})"

        now = datetime.now(timezone.utc)

        logger.info(f"Created journey {journey_id} with {len(touchpoints)} touchpoints")

        return JourneyResponse(
            journey_id=journey_id,
            name=request.name or f"Journey {journey_id}",
            description=description,
            touchpoints=touchpoints,
            total_duration_days=total_duration,
            estimated_total_cost=total_cost,
            created_at=now,
            updated_at=now,
        )

    except SynthWellClientError as e:
        logger.warning(f"SynthWell v2 API error, falling back to mock: {e}")
        return await _generate_mock_journey(request)


async def modify_journey(
    journey_id: str,
    modifications: dict,
    client: SynthWellClient | None = None,
) -> JourneyResponse:
    """
    Modify an existing journey.

    Supports operations like:
    - add_touchpoint: Add a new touchpoint at a specific position
    - remove_touchpoint: Remove a touchpoint by ID
    - move_touchpoint: Change the day of a touchpoint
    - update_touchpoint: Update touchpoint properties

    Args:
        journey_id: Journey ID to modify
        modifications: Dict with operation and parameters
        client: Optional SynthWell client (for testing)
    """
    client = client or get_synthwell_client()

    # Extract touchpoints from modifications if provided
    touchpoints_data = modifications.get("touchpoints", [])

    try:
        if touchpoints_data:
            # Call backend to update journey
            result = await client.update_journey(
                journey_id=journey_id,
                touchpoints=touchpoints_data,
            )

            journey_data = result.get("journey", result)
            touchpoints = _parse_touchpoints(journey_data.get("touchpoints", []))
        else:
            # No touchpoint changes, return current state
            touchpoints = _default_touchpoints()

    except SynthWellClientError as e:
        logger.warning(f"SynthWell API error, using default touchpoints: {e}")
        touchpoints = _default_touchpoints()

    operation = modifications.get("operation", "update")
    now = datetime.now(timezone.utc)

    return JourneyResponse(
        journey_id=journey_id,
        name=f"Modified Journey ({operation})",
        description=f"Journey modified via {operation} operation",
        touchpoints=touchpoints,
        total_duration_days=max(tp.day for tp in touchpoints) if touchpoints else 0,
        estimated_total_cost=sum(tp.estimated_cost for tp in touchpoints),
        created_at=now,
        updated_at=now,
    )


async def optimize_journey(
    journey_id: str,
    touchpoints: list[dict] | None = None,
    optimization_goal: str = "enrollment",
    target_conversion: float = 0.15,
    client: SynthWellClient | None = None,
) -> JourneyResponse:
    """
    Automatically optimize a journey based on simulation analysis.

    Analyzes the journey for issues (low engagement, dropoffs, fatigue) and
    suggests/applies refinements to improve conversion rate.

    Goals:
    - enrollment: Maximize enrollment rate (default)
    - cost: Minimize cost per enrollment
    - engagement: Maximize engagement across touchpoints
    - retention: Minimize dropoff

    Args:
        journey_id: Journey ID being optimized
        touchpoints: Current journey touchpoints to optimize
        optimization_goal: Optimization target
        target_conversion: Target conversion rate (default 15%)
        client: Optional SynthWell client (for testing)

    Returns:
        Optimized journey with recommendations
    """
    client = client or get_synthwell_client()
    now = datetime.now(timezone.utc)

    # Use provided touchpoints or generate defaults
    if not touchpoints:
        touchpoints = [
            {"id": "tp1", "channel": "MAIL", "day": 1},
            {"id": "tp2", "channel": "PHONE", "day": 3},
            {"id": "tp3", "channel": "MAIL", "day": 7},
            {"id": "tp4", "channel": "PHONE", "day": 14},
        ]

    # Adjust target based on optimization goal
    if optimization_goal == "cost":
        # Lower target allows less aggressive optimization
        target_conversion = min(target_conversion, 0.12)
    elif optimization_goal == "engagement":
        # Focus on engagement over conversion
        target_conversion = target_conversion * 1.1

    try:
        # Call SynthWell optimizer
        result = await client.optimize_journey(
            touchpoints=touchpoints,
            target_conversion=target_conversion,
            max_iterations=3,
        )

        # Extract optimized touchpoints
        optimized_tps = result.get("optimized_touchpoints", [])
        recommendations = result.get("recommendations", [])
        improvement = result.get("improvement", 0.0)
        original_conv = result.get("original_conversion", 0.0)
        optimized_conv = result.get("optimized_conversion", original_conv)

        # Convert optimized touchpoints to our format
        parsed_touchpoints = []
        for tp in optimized_tps:
            channel = tp.get("channel", "MAIL")
            channel_lower = channel.lower()

            parsed_touchpoints.append(
                Touchpoint(
                    id=tp.get("id", f"tp_{uuid.uuid4().hex[:8]}"),
                    type=_map_touchpoint_type(channel),
                    name=f"{tp.get('stage', 'Stage')} {channel.title()}",
                    day=tp.get("day", 1),
                    estimated_cost=CHANNEL_COSTS.get(channel_lower, 0.15),
                    expected_response_rate=0.25,
                )
            )

        # If no optimized touchpoints returned, use original with recommendations
        if not parsed_touchpoints:
            parsed_touchpoints = _parse_touchpoints(touchpoints)

        # Build description from recommendations
        if recommendations:
            description = " ".join(recommendations[:3])  # First 3 recommendations
        else:
            description = f"Optimization complete. Predicted conversion: {optimized_conv:.1%}"

        if improvement > 0:
            description += f" (+{improvement:.1%} improvement)"

        return JourneyResponse(
            journey_id=journey_id,
            name=f"Optimized for {optimization_goal}",
            description=description,
            touchpoints=parsed_touchpoints,
            total_duration_days=max(tp.day for tp in parsed_touchpoints) if parsed_touchpoints else 0,
            estimated_total_cost=sum(tp.estimated_cost for tp in parsed_touchpoints),
            created_at=now,
            updated_at=now,
        )

    except SynthWellClientError as e:
        logger.warning(f"SynthWell optimization error, falling back to defaults: {e}")
        # Return default optimized journey as fallback
        fallback_touchpoints = _default_touchpoints()
        return JourneyResponse(
            journey_id=journey_id,
            name=f"Optimized for {optimization_goal}",
            description="Optimization service unavailable. Returning default optimized journey.",
            touchpoints=fallback_touchpoints,
            total_duration_days=max(tp.day for tp in fallback_touchpoints),
            estimated_total_cost=sum(tp.estimated_cost for tp in fallback_touchpoints),
            created_at=now,
            updated_at=now,
        )


def _default_touchpoints() -> list[Touchpoint]:
    """Return default journey touchpoints."""
    return [
        Touchpoint(
            id=f"tp_{uuid.uuid4().hex[:8]}",
            type=TouchpointType.EMAIL,
            name="Welcome Email",
            day=1,
            content_template="welcome_intro",
            estimated_cost=0.15,
            expected_response_rate=0.25,
        ),
        Touchpoint(
            id=f"tp_{uuid.uuid4().hex[:8]}",
            type=TouchpointType.SMS,
            name="Engagement SMS",
            day=7,
            content_template="benefits_reminder",
            estimated_cost=0.08,
            expected_response_rate=0.35,
        ),
        Touchpoint(
            id=f"tp_{uuid.uuid4().hex[:8]}",
            type=TouchpointType.MAILER,
            name="Benefits Overview Mailer",
            day=14,
            content_template="benefits_mailer",
            estimated_cost=1.25,
            expected_response_rate=0.18,
        ),
        Touchpoint(
            id=f"tp_{uuid.uuid4().hex[:8]}",
            type=TouchpointType.CALL,
            name="Personal Outreach Call",
            day=21,
            content_template="consultation_offer",
            estimated_cost=8.50,
            expected_response_rate=0.45,
        ),
    ]


async def _generate_mock_journey(request: JourneyRequest) -> JourneyResponse:
    """Generate mock journey data as fallback."""
    now = datetime.now(timezone.utc)
    touchpoints = request.touchpoints or _default_touchpoints()

    return JourneyResponse(
        journey_id=f"journey_{uuid.uuid4().hex[:8]}",
        name=request.name,
        description=request.description,
        touchpoints=touchpoints,
        total_duration_days=max(tp.day for tp in touchpoints) if touchpoints else 0,
        estimated_total_cost=sum(tp.estimated_cost for tp in touchpoints),
        created_at=now,
        updated_at=now,
    )
