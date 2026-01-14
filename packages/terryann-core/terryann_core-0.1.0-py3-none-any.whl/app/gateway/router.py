"""Gateway router for conversation endpoints."""

import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.gateway.auth import TokenPayload, get_current_user
from app.gateway.session import conversation_manager, generate_session_id
from app.mcp.server import MCPServer
from app.mcp.tools.cohort import generate_cohort, extract_location_hint
from app.mcp.tools.journey import create_journey, optimize_journey
from app.mcp.tools.simulation import simulate_journey_changes, create_modified_touchpoints
from app.clients.synthwell_client import get_synthwell_client, SynthWellClientError
from app.models.schemas import (
    MessageRequest,
    MessageResponse,
    CohortRequest,
    JourneyRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gateway", tags=["gateway"])


# =============================================================================
# Journey Parameter Extraction Helpers
# =============================================================================

def _extract_zip_codes(text: str) -> list[str]:
    """Extract ZIP codes from text."""
    import re
    # Match 5-digit ZIP codes
    zip_pattern = r'\b(\d{5})\b'
    return re.findall(zip_pattern, text)


def _extract_campaign_type(text: str) -> str | None:
    """Extract campaign type from text."""
    text_lower = text.lower()

    campaign_types = {
        "aep": "AEP_ACQUISITION",
        "annual enrollment": "AEP_ACQUISITION",
        "oep": "OEP_RETENTION",
        "open enrollment": "OEP_RETENTION",
        "sep": "SEP_ACQUISITION",
        "special enrollment": "SEP_ACQUISITION",
        "retention": "OEP_RETENTION",
        "acquisition": "AEP_ACQUISITION",
        "win-back": "WINBACK",
        "winback": "WINBACK",
        "re-engagement": "WINBACK",
    }

    for keyword, campaign_type in campaign_types.items():
        if keyword in text_lower:
            return campaign_type
    return None


def _extract_location_from_conversation(messages: list[dict]) -> dict[str, Any]:
    """
    Extract location info from conversation history.

    Returns dict with:
    - zip_codes: list of ZIP codes found
    - city: city name if mentioned (with state code for resolution)
    - state: state code if mentioned
    - region: region name if mentioned
    - national: bool if national targeting mentioned
    - location_type: best location type detected (zip, city, state, region, national)
    - location_value: value for resolution API
    """
    location_info = {
        "zip_codes": [],
        "city": None,
        "city_state": None,  # For resolution API: "Miami|FL"
        "state": None,
        "region": None,
        "national": False,
        "location_type": None,
        "location_value": None,
    }

    # Extended city list with state mappings
    city_state_map = {
        # Florida
        "miami": "FL", "tampa": "FL", "orlando": "FL", "jacksonville": "FL",
        "fort lauderdale": "FL", "west palm beach": "FL", "naples": "FL",
        # Arizona
        "phoenix": "AZ", "tucson": "AZ", "scottsdale": "AZ", "mesa": "AZ",
        # Texas
        "houston": "TX", "dallas": "TX", "san antonio": "TX", "austin": "TX",
        "fort worth": "TX", "el paso": "TX",
        # California
        "los angeles": "CA", "san diego": "CA", "san francisco": "CA",
        "san jose": "CA", "fresno": "CA", "sacramento": "CA",
        # New York
        "new york": "NY", "brooklyn": "NY", "queens": "NY", "buffalo": "NY",
        # Midwest
        "chicago": "IL", "detroit": "MI", "cleveland": "OH", "columbus": "OH",
        "indianapolis": "IN", "milwaukee": "WI", "minneapolis": "MN",
        # Southeast
        "atlanta": "GA", "charlotte": "NC", "raleigh": "NC", "nashville": "TN",
        "memphis": "TN", "birmingham": "AL", "new orleans": "LA",
        # West
        "denver": "CO", "las vegas": "NV", "seattle": "WA", "portland": "OR",
        "salt lake city": "UT", "albuquerque": "NM",
        # Northeast
        "philadelphia": "PA", "pittsburgh": "PA", "boston": "MA", "baltimore": "MD",
    }

    # State codes and names
    state_map = {
        "alabama": "AL", "al": "AL", "alaska": "AK", "ak": "AK",
        "arizona": "AZ", "az": "AZ", "arkansas": "AR", "ar": "AR",
        "california": "CA", "ca": "CA", "colorado": "CO", "co": "CO",
        "connecticut": "CT", "ct": "CT", "delaware": "DE", "de": "DE",
        "florida": "FL", "fl": "FL", "georgia": "GA", "ga": "GA",
        "hawaii": "HI", "hi": "HI", "idaho": "ID", "id": "ID",
        "illinois": "IL", "il": "IL", "indiana": "IN", "in": "IN",
        "iowa": "IA", "ia": "IA", "kansas": "KS", "ks": "KS",
        "kentucky": "KY", "ky": "KY", "louisiana": "LA", "la": "LA",
        "maine": "ME", "me": "ME", "maryland": "MD", "md": "MD",
        "massachusetts": "MA", "ma": "MA", "michigan": "MI", "mi": "MI",
        "minnesota": "MN", "mn": "MN", "mississippi": "MS", "ms": "MS",
        "missouri": "MO", "mo": "MO", "montana": "MT", "mt": "MT",
        "nebraska": "NE", "ne": "NE", "nevada": "NV", "nv": "NV",
        "new hampshire": "NH", "nh": "NH", "new jersey": "NJ", "nj": "NJ",
        "new mexico": "NM", "nm": "NM", "new york": "NY", "ny": "NY",
        "north carolina": "NC", "nc": "NC", "north dakota": "ND", "nd": "ND",
        "ohio": "OH", "oh": "OH", "oklahoma": "OK", "ok": "OK",
        "oregon": "OR", "or": "OR", "pennsylvania": "PA", "pa": "PA",
        "rhode island": "RI", "ri": "RI", "south carolina": "SC", "sc": "SC",
        "south dakota": "SD", "sd": "SD", "tennessee": "TN", "tn": "TN",
        "texas": "TX", "tx": "TX", "utah": "UT", "ut": "UT",
        "vermont": "VT", "vt": "VT", "virginia": "VA", "va": "VA",
        "washington": "WA", "wa": "WA", "west virginia": "WV", "wv": "WV",
        "wisconsin": "WI", "wi": "WI", "wyoming": "WY", "wy": "WY",
    }

    # Regions
    regions = ["northeast", "southeast", "midwest", "southwest", "west"]

    # Search through all messages
    for msg in messages:
        content = msg.get("content", "").lower()

        # Extract ZIP codes
        zips = _extract_zip_codes(content)
        location_info["zip_codes"].extend(zips)

        # Check for national targeting
        if any(word in content for word in ["national", "nationwide", "all states", "entire country", "usa"]):
            location_info["national"] = True

        # Check for region mentions
        for region in regions:
            if region in content:
                location_info["region"] = region
                break

        # Check for city mentions (longer names first to match "new york" before "york")
        for city in sorted(city_state_map.keys(), key=len, reverse=True):
            if city in content:
                location_info["city"] = city.title()
                location_info["city_state"] = f"{city.title()}|{city_state_map[city]}"
                break

        # Check for state mentions
        for state_name, state_code in state_map.items():
            if state_name in content:
                location_info["state"] = state_code
                break

    # Deduplicate ZIP codes
    location_info["zip_codes"] = list(set(location_info["zip_codes"]))

    # Determine best location type and value (priority: zip > city > state > region > national)
    if location_info["zip_codes"]:
        location_info["location_type"] = "zip"
        location_info["location_value"] = location_info["zip_codes"][0]
    elif location_info["city"]:
        location_info["location_type"] = "city"
        location_info["location_value"] = location_info["city_state"]
    elif location_info["state"]:
        location_info["location_type"] = "state"
        location_info["location_value"] = location_info["state"]
    elif location_info["region"]:
        location_info["location_type"] = "region"
        location_info["location_value"] = location_info["region"]
    elif location_info["national"]:
        location_info["location_type"] = "national"
        location_info["location_value"] = "national"

    return location_info


async def _analyze_geography(
    location_type: str,
    location_value: str,
) -> dict[str, Any]:
    """
    Analyze a geographic area and return market clusters.

    Args:
        location_type: Type of location (state, region, national, city, zip)
        location_value: Location value for analysis

    Returns:
        Analysis response with clusters, or empty dict on error
    """
    from app.clients.synthwell_client import get_synthwell_client, SynthWellClientError

    try:
        client = get_synthwell_client()
        return await client.analyze_geography(
            location_type=location_type,
            location_value=location_value,
        )
    except SynthWellClientError as e:
        logger.warning(f"Failed to analyze geography {location_type}={location_value}: {e}")
        return {}


async def _resolve_location_to_zips(
    location_type: str,
    location_value: str,
    cluster_id: str | None = None,
    max_zips: int = 10,
) -> list[str]:
    """
    Resolve a semantic location to ZIP codes via backend API.

    Args:
        location_type: Type of location (zip, city, state, region, national)
        location_value: Location value for resolution
        cluster_id: Optional cluster ID for targeted resolution
        max_zips: Maximum ZIPs to return

    Returns:
        List of ZIP codes, or empty list on error
    """
    from app.clients.synthwell_client import get_synthwell_client, SynthWellClientError

    if location_type == "zip":
        return [location_value.zfill(5)]

    try:
        client = get_synthwell_client()
        result = await client.resolve_location(
            location_type=location_type,
            location_value=location_value,
            cluster_id=cluster_id,
            max_zips=max_zips,
        )
        return result.get("zip_codes", [])
    except SynthWellClientError as e:
        logger.warning(f"Failed to resolve location {location_type}={location_value}: {e}")
        return []


def _format_clusters_for_display(clusters: list[dict], location_label: str) -> str:
    """Format cluster options for TerryAnn to present to user."""
    if not clusters:
        return ""

    lines = [f"**{location_label}** has {len(clusters)} distinct market segments:\n"]

    for i, cluster in enumerate(clusters, 1):
        label = cluster.get("label", "Unknown")
        description = cluster.get("description", "")
        zip_count = cluster.get("zip_count", 0)
        traits = cluster.get("traits", {})

        # Format key traits
        trait_highlights = []
        if traits.get("income_level"):
            trait_highlights.append(traits["income_level"].replace("_", " ").title())
        if traits.get("urbanicity"):
            trait_highlights.append(traits["urbanicity"].title())
        if traits.get("primary_language") and traits["primary_language"] != "English":
            trait_highlights.append(f"{traits['primary_language']}-speaking")

        trait_str = ", ".join(trait_highlights) if trait_highlights else ""

        lines.append(f"**{i}. {label}**")
        if description:
            lines.append(f"   {description}")
        if trait_str:
            lines.append(f"   *{trait_str}* | {zip_count:,} ZIPs")
        lines.append("")

    lines.append("Which market segment would you like to target? (Enter the number, or 'all' for a sample across segments)")

    return "\n".join(lines)


# Campaign types with user-friendly display
CAMPAIGN_TYPE_OPTIONS = [
    {"id": "aep_acquisition", "label": "AEP Acquisition", "description": "Annual Enrollment Period - acquire new members (Oct 15 - Dec 7)"},
    {"id": "turning_65", "label": "Turning 65", "description": "Target prospects aging into Medicare eligibility"},
    {"id": "retention", "label": "Retention (OEP)", "description": "Keep existing members during Open Enrollment (Jan 1 - Mar 31)"},
    {"id": "onboarding", "label": "New Member Onboarding", "description": "Welcome and activate new enrollees"},
    {"id": "benefit_utilization", "label": "Benefit Utilization", "description": "Drive usage of plan benefits (AWV, OTC, fitness)"},
    {"id": "gap_closure", "label": "Care Gap Closure", "description": "Close HEDIS gaps for Star Ratings improvement"},
]


def _format_campaign_types_for_display(location_name: str) -> str:
    """Format campaign type options for TerryAnn to present to user."""
    lines = [f"What type of campaign would you like to create for **{location_name}**?\n"]

    for i, campaign in enumerate(CAMPAIGN_TYPE_OPTIONS, 1):
        lines.append(f"**{i}. {campaign['label']}**")
        lines.append(f"   {campaign['description']}")
        lines.append("")

    lines.append("Enter the number of your choice:")

    return "\n".join(lines)


def _extract_journey_params_from_conversation(messages: list[dict]) -> dict[str, Any]:
    """
    Extract journey creation parameters from conversation history.

    Returns dict with:
    - name: journey name (if mentioned)
    - zip_codes: target ZIP codes
    - campaign_type: campaign type
    - location_description: human-readable location
    - location_type: type for resolution (zip, city, state, region, national)
    - location_value: value for resolution API
    - ready: bool indicating if we have enough info
    - missing: list of what's still needed
    """
    params = {
        "name": None,
        "zip_codes": [],
        "campaign_type": None,
        "location_description": None,
        "location_type": None,
        "location_value": None,
        "ready": False,
        "missing": [],
    }

    # Extract location info
    location_info = _extract_location_from_conversation(messages)
    params["zip_codes"] = location_info["zip_codes"]
    params["location_type"] = location_info["location_type"]
    params["location_value"] = location_info["location_value"]

    # Build location description
    if location_info["city"]:
        params["location_description"] = location_info["city"]
    elif location_info["state"]:
        params["location_description"] = location_info["state"]
    elif location_info["region"]:
        params["location_description"] = location_info["region"].title()
    elif location_info["national"]:
        params["location_description"] = "National"
    elif params["zip_codes"]:
        params["location_description"] = f"ZIP {', '.join(params['zip_codes'][:3])}"

    # Extract campaign type from all messages
    for msg in messages:
        content = msg.get("content", "")
        if not params["campaign_type"]:
            params["campaign_type"] = _extract_campaign_type(content)

    # Check what's missing - now includes region and national
    has_location = (
        params["zip_codes"] or
        location_info["city"] or
        location_info["state"] or
        location_info["region"] or
        location_info["national"]
    )
    if not has_location:
        params["missing"].append("target location (ZIP codes, city, state, region, or national)")

    if not params["campaign_type"]:
        params["missing"].append("campaign type (AEP, OEP, retention, etc.)")

    # Ready if we have any location
    params["ready"] = len(params["missing"]) == 0 or has_location

    # Default campaign type if we have location but no type specified
    if params["ready"] and not params["campaign_type"]:
        params["campaign_type"] = "AEP_ACQUISITION"

    # Generate journey name if not provided
    if not params["name"] and params["location_description"]:
        campaign_display = {
            "AEP_ACQUISITION": "AEP",
            "OEP_RETENTION": "OEP Retention",
            "SEP_ACQUISITION": "SEP",
            "WINBACK": "Win-back",
        }
        type_name = campaign_display.get(params["campaign_type"], "Campaign")
        params["name"] = f"{params['location_description']} {type_name} Journey"

    return params


def _should_create_journey(terryann_response: str, conversation_messages: list[dict]) -> bool:
    """
    Detect if TerryAnn's response indicates she's ready to create a journey.

    Looks for patterns like:
    - "Let me create that journey"
    - "I'll generate a journey"
    - "Creating your journey now"
    - User said "yes" / "go ahead" after TerryAnn asked if ready
    """
    response_lower = terryann_response.lower()

    # Check for creation intent in TerryAnn's response
    creation_phrases = [
        "let me create",
        "i'll create",
        "i will create",
        "creating your journey",
        "generating your journey",
        "let me generate",
        "i'll generate",
        "i have everything i need",
        "i have all the information",
        "ready to create",
    ]

    for phrase in creation_phrases:
        if phrase in response_lower:
            return True

    # Check if user just confirmed and TerryAnn previously offered to create
    if conversation_messages:
        last_user_msg = None
        last_assistant_msg = None

        for msg in reversed(conversation_messages):
            if msg.get("role") == "user" and not last_user_msg:
                last_user_msg = msg.get("content", "").lower()
            elif msg.get("role") == "assistant" and not last_assistant_msg:
                last_assistant_msg = msg.get("content", "").lower()
            if last_user_msg and last_assistant_msg:
                break

        # If user confirmed and assistant was asking about journey creation
        if last_user_msg and last_assistant_msg:
            user_confirmed = any(word in last_user_msg for word in ["yes", "yeah", "sure", "go ahead", "please", "ok"])
            assistant_offered = any(phrase in last_assistant_msg for phrase in [
                "create a journey",
                "generate a journey",
                "shall i create",
                "would you like me to create",
                "ready to create",
            ])

            if user_confirmed and assistant_offered:
                return True

    return False

# Initialize MCP server
mcp_server = MCPServer()


@router.post("/message", response_model=MessageResponse)
async def handle_message(
    request: MessageRequest,
    user: Annotated[TokenPayload | None, Depends(get_current_user)],
) -> MessageResponse:
    """
    Handle a user message and return TerryAnn's response.

    This endpoint:
    1. Creates or retrieves a conversation from Supabase
    2. Processes the user message
    3. Invokes MCP tools as needed (calls SynthWell backend)
    4. Persists state updates
    5. Returns the response with metadata
    """
    # Generate session_id if not provided
    session_id = request.session_id or generate_session_id()

    # Get or create conversation in Supabase
    conversation = await conversation_manager.get_or_create_conversation(
        session_id=session_id,
        surface=request.surface,
        user_id=user.sub if user else None,
    )

    # Get existing messages for context
    existing_messages = conversation.state.get("messages", [])

    # Infer intent from message with conversation context
    current_intent = _infer_intent(request.message, existing_messages, conversation.state)

    # Execute tools and generate response
    tools_used = []
    tool_results: dict[str, Any] = {}
    response_text = await _process_message_with_tools(
        message=request.message,
        intent=current_intent,
        conversation_state=conversation.state,
        tools_used=tools_used,
        tool_results=tool_results,
        user_id=user.sub if user else None,
        surface=request.surface,
    )

    # Update conversation state with message history
    messages = existing_messages.copy()
    messages.append({"role": "user", "content": request.message})
    messages.append({
        "role": "assistant",
        "content": response_text,
        "tools_used": tools_used,
        "tool_results": tool_results,
    })

    # Persist state update to Supabase
    await conversation_manager.update_conversation_state(
        conversation_id=conversation.id,
        state={
            "messages": messages,
            "last_tools_used": tools_used,
            "last_tool_results": tool_results,
            **(request.context or {}),
        },
        current_intent=current_intent,
    )

    return MessageResponse(
        response=response_text,
        session_id=session_id,
        tools_used=tools_used,
        metadata={
            "model": "synthwell",
            "conversation_id": conversation.id,
            "surface": conversation.surface,
            "message_count": len(messages),
            "tool_results": tool_results,
        },
    )


@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    user: Annotated[TokenPayload | None, Depends(get_current_user)],
):
    """Get session details and conversation history."""
    conversation = await conversation_manager.get_conversation_by_session(session_id)
    if not conversation:
        return {"error": "Session not found"}

    messages = conversation.state.get("messages", [])

    return {
        "session_id": conversation.session_id,
        "conversation_id": conversation.id,
        "surface": conversation.surface,
        "current_intent": conversation.current_intent,
        "created_at": conversation.created_at.isoformat(),
        "updated_at": conversation.updated_at.isoformat(),
        "message_count": len(messages),
        "messages": [
            {
                "role": m.get("role"),
                "content": m.get("content", "")[:100] + "..."
                if len(m.get("content", "")) > 100
                else m.get("content", ""),
            }
            for m in messages[-10:]  # Last 10 messages
        ],
    }


@router.get("/tools")
async def list_tools():
    """List available MCP tools."""
    return {"tools": mcp_server.list_tools()}


@router.get("/journeys")
async def list_journeys(
    limit: int = 20,
    user: Annotated[TokenPayload | None, Depends(get_current_user)] = None,
):
    """List recent journeys."""
    journeys = await conversation_manager.list_journeys(limit=limit)
    return {
        "journeys": [
            {
                "id": j.id,
                "status": j.status,
                "cohort_config": j.cohort_config,
                "journey_data": j.journey_data,
                "created_at": j.created_at.isoformat(),
                "updated_at": j.updated_at.isoformat(),
            }
            for j in journeys
        ],
        "count": len(journeys),
    }


@router.get("/journeys/{journey_id}")
async def get_journey(
    journey_id: str,
    user: Annotated[TokenPayload | None, Depends(get_current_user)] = None,
):
    """Get journey by ID."""
    journey = await conversation_manager.get_journey(journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    return {
        "id": journey.id,
        "status": journey.status,
        "cohort_config": journey.cohort_config,
        "journey_data": journey.journey_data,
        "simulation_results": journey.simulation_results,
        "created_at": journey.created_at.isoformat(),
        "updated_at": journey.updated_at.isoformat(),
    }


def _is_affirmative(message: str) -> bool:
    """Check if message is an affirmative continuation response."""
    affirmatives = {
        "yes", "yeah", "yep", "sure", "ok", "okay", "go ahead", "do it",
        "please", "sounds good", "let's do it", "proceed", "continue",
        "yes please", "absolutely", "definitely", "y", "yea",
    }
    return message.lower().strip().rstrip(".!") in affirmatives


def _infer_next_action_from_context(messages: list[dict]) -> str | None:
    """
    Infer the next action based on what TerryAnn last offered.

    Looks at the last assistant message for offers like:
    - "Would you like me to create a journey?" -> create_journey
    - "Shall I simulate this journey?" -> simulate_journey
    - "Would you like me to optimize?" -> optimize_journey
    """
    if not messages:
        return None

    # Find last assistant message
    last_assistant_msg = None
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            last_assistant_msg = msg.get("content", "").lower()
            break

    if not last_assistant_msg:
        return None

    # Check what was offered
    # Journey creation - TerryAnn may say "create a journey", "ready to generate", etc.
    journey_creation_phrases = [
        "create a journey",
        "would you like me to create",
        "ready to generate",
        "ready to create",
        "shall i generate",
        "shall i create",
    ]
    if any(phrase in last_assistant_msg for phrase in journey_creation_phrases):
        return "create_journey"

    # Simulation
    if "simulate" in last_assistant_msg and ("shall i" in last_assistant_msg or "would you like" in last_assistant_msg):
        return "simulate_journey"

    # Optimization
    if "optimize" in last_assistant_msg and ("shall i" in last_assistant_msg or "would you like" in last_assistant_msg):
        return "optimize_journey"

    return None


def _infer_intent(
    message: str,
    messages: list[dict] | None = None,
    conversation_state: dict[str, Any] | None = None,
) -> str | None:
    """
    Infer user intent from message and conversation context.

    Args:
        message: Current user message
        messages: Previous conversation messages for context
        conversation_state: Full conversation state for checking pending actions
    """
    message_lower = message.lower().strip()

    # Check for pending selections - user responding with number or "all"
    if conversation_state:
        last_results = conversation_state.get("last_tool_results", {})

        # Check for pending campaign type selection
        pending_campaign_type = last_results.get("pending_campaign_type_selection", {})
        if pending_campaign_type:
            if message_lower.isdigit():
                logger.info(f"Intent detection: campaign type selection response -> create_journey")
                return "create_journey"

        # Check for pending cluster selection
        pending_cluster = last_results.get("pending_cluster_selection", {})
        if pending_cluster:
            # User is responding to cluster selection prompt
            if message_lower.isdigit() or "all" in message_lower:
                logger.info(f"Intent detection: cluster selection response -> create_journey")
                return "create_journey"

    # Check for affirmative response to continue previous flow
    if _is_affirmative(message) and messages:
        intent = _infer_next_action_from_context(messages)
        logger.info(f"Intent detection: affirmative response, next_action={intent}")
        return intent

    if "cohort" in message_lower or "segment" in message_lower:
        logger.info("Intent detection: cohort/segment keyword -> generate_cohort")
        return "generate_cohort"
    if "simulate" in message_lower or "simulation" in message_lower or "what if" in message_lower:
        logger.info(f"Intent detection: simulate/what-if keyword -> simulate_journey (message: {message[:50]})")
        return "simulate_journey"
    if "optimize" in message_lower:
        logger.info("Intent detection: optimize keyword -> optimize_journey")
        return "optimize_journey"
    # Detect journey/campaign creation with enough context (location provided)
    has_journey_word = "journey" in message_lower or "campaign" in message_lower
    has_create_word = "create" in message_lower or "build" in message_lower or "make" in message_lower
    if has_journey_word and has_create_word:
        # Check if we have location info - extract from just this message
        location_info = _extract_location_from_conversation([{"content": message}])
        has_location = (
            location_info["zip_codes"] or
            location_info["city"] or
            location_info["state"] or
            location_info["region"] or
            location_info["national"]
        )
        if has_location:
            logger.info(f"Intent detection: journey/campaign creation with location ({location_info['location_type']}) -> create_journey")
            return "create_journey"
    if "push" in message_lower or "crm" in message_lower:
        return "push_to_crm"
    if "schedule" in message_lower and "campaign" in message_lower:
        return "schedule_campaign"

    logger.info(f"Intent detection: no keyword match, returning None (message: {message[:50]})")
    return None


async def _process_message_with_tools(
    message: str,
    intent: str | None,
    conversation_state: dict[str, Any],
    tools_used: list[str],
    tool_results: dict[str, Any],
    user_id: str | None = None,
    surface: str = "web",
) -> str:
    """
    Process a message by invoking appropriate tools.

    Calls the SynthWell backend via MCP tools and formats the response.

    Args:
        message: User message
        intent: Detected intent
        conversation_state: Current conversation state
        tools_used: List to append tool names to
        tool_results: Dict to store tool results
        user_id: Optional user ID for journey ownership
        surface: Source surface (e.g., 'cli', 'web')
    """
    message_lower = message.lower()

    # Handle cohort generation
    if intent == "generate_cohort" or "cohort" in message_lower or "segment" in message_lower:
        tools_used.append("generate_cohort")
        try:
            cohort_request = CohortRequest(size=1000)
            result = await generate_cohort(request=cohort_request, message=message)

            # Store result summary
            tool_results["cohort"] = {
                "cohort_id": result.cohort_id,
                "name": result.name,
                "size": result.size,
                "summary": result.summary,
            }

            # Extract location for response
            location = extract_location_hint(message) or "the target area"

            return (
                f"I've generated a cohort for {location}. The cohort '{result.name}' includes "
                f"{result.size:,} Medicare-eligible individuals with an average age of "
                f"{result.summary.get('avg_age', 72)} and moderate risk profiles.\n\n"
                f"**Cohort ID:** `{result.cohort_id}`\n"
                f"**Channel Distribution:** Email {result.summary.get('channel_distribution', {}).get('email', 0.45):.0%}, "
                f"SMS {result.summary.get('channel_distribution', {}).get('sms', 0.30):.0%}, "
                f"Mailer {result.summary.get('channel_distribution', {}).get('mailer', 0.25):.0%}\n\n"
                "Would you like me to create a journey for this cohort?"
            )
        except Exception as e:
            logger.error(f"Error generating cohort: {e}")
            return f"I encountered an error generating the cohort: {str(e)}. Please try again."

    # Handle simulation ("what if" scenarios)
    simulate_check = intent == "simulate_journey" or "simulate" in message_lower or "what if" in message_lower
    logger.info(f"Simulation check: intent={intent}, 'simulate' in msg={'simulate' in message_lower}, 'what if' in msg={'what if' in message_lower}, result={simulate_check}")
    if simulate_check:
        tools_used.append("simulate_journey")
        logger.info("Entering simulation handler")
        try:
            # Get journey from conversation state
            last_results = conversation_state.get("last_tool_results", {})
            journey_data = last_results.get("journey", {})
            journey_id = journey_data.get("journey_id", "journey_default")

            # Get baseline touchpoints from conversation state or use defaults
            baseline_touchpoints = journey_data.get("touchpoints_for_simulation")
            if not baseline_touchpoints:
                baseline_touchpoints = [
                    {"id": "tp_1", "channel": "direct_mail", "day": 1, "stage": "Awareness"},
                    {"id": "tp_2", "channel": "email", "day": 7, "stage": "Consideration"},
                    {"id": "tp_3", "channel": "sms", "day": 14, "stage": "Decision"},
                    {"id": "tp_4", "channel": "phone_outbound", "day": 21, "stage": "Enrollment"},
                ]

            # Parse modification from message
            # Example: "what if we add a mailer on day 3?"
            # Example: "what if we remove the phone call?"
            # Example: "what if we change the email to SMS?"
            import re

            modified_touchpoints = baseline_touchpoints.copy()
            modification_description = "no changes"

            # Check for "add" modifications
            add_match = re.search(r'add\s+(?:a\s+)?(\w+)(?:\s+on)?\s+day\s+(\d+)', message_lower)
            if add_match:
                channel_hint = add_match.group(1)
                day = int(add_match.group(2))

                # Map common terms to channel names
                channel_map = {
                    "mailer": "direct_mail", "mail": "direct_mail",
                    "email": "email", "sms": "sms", "text": "sms",
                    "phone": "phone_outbound", "call": "phone_outbound",
                }
                channel = channel_map.get(channel_hint, channel_hint)

                new_tp = {"id": f"tp_new_{day}", "channel": channel, "day": day, "stage": "Consideration"}
                modified_touchpoints = create_modified_touchpoints(
                    baseline=baseline_touchpoints,
                    add=[new_tp]
                )
                modification_description = f"adding {channel} on day {day}"

            # Check for "remove" modifications
            remove_match = re.search(r'remove\s+(?:the\s+)?(\w+)', message_lower)
            if remove_match:
                channel_hint = remove_match.group(1)
                channel_map = {
                    "mailer": "direct_mail", "mail": "direct_mail",
                    "email": "email", "sms": "sms", "text": "sms",
                    "phone": "phone_outbound", "call": "phone_outbound",
                }
                channel = channel_map.get(channel_hint, channel_hint)

                # Find and remove touchpoint with this channel
                remove_ids = [tp["id"] for tp in baseline_touchpoints if tp.get("channel") == channel]
                if remove_ids:
                    modified_touchpoints = create_modified_touchpoints(
                        baseline=baseline_touchpoints,
                        remove_ids=remove_ids
                    )
                    modification_description = f"removing {channel}"

            # Run simulation comparing baseline vs modified
            result = await simulate_journey_changes(
                journey_id=journey_id,
                baseline_touchpoints=baseline_touchpoints,
                modified_touchpoints=modified_touchpoints,
            )

            tool_results["simulation"] = {
                "journey_id": result.journey_id,
                "baseline_enrollment": result.baseline.total_advance_probability,
                "modified_enrollment": result.modified.total_advance_probability,
                "delta": {
                    "enrollment_change": result.delta.advance_probability_change,
                    "dropout_change": result.delta.dropout_probability_change,
                    "cost_change": result.delta.cost_change,
                    "interpretation": result.delta.interpretation,
                },
            }

            # Format friendly response
            baseline_pct = result.baseline.total_advance_probability * 100
            modified_pct = result.modified.total_advance_probability * 100
            change_pct = result.delta.advance_probability_change * 100
            change_direction = "increases" if change_pct > 0 else "decreases"

            return (
                f"I simulated the impact of {modification_description}.\n\n"
                f"**Results:**\n"
                f"- Baseline enrollment: {baseline_pct:.1f}%\n"
                f"- With change: {modified_pct:.1f}%\n"
                f"- **Enrollment {change_direction} by {abs(change_pct):.1f}%**\n\n"
                f"**Analysis:** {result.delta.interpretation}\n\n"
                "Would you like to try another scenario?"
            )
        except Exception as e:
            logger.error(f"Error running simulation: {e}", exc_info=True)
            return f"I encountered an error running the simulation: {str(e)}. Please try again."

    # Handle journey creation (direct from message or continuation from previous flow)
    if intent == "create_journey":
        tools_used.append("create_journey")
        try:
            # Get data from conversation state
            last_results = conversation_state.get("last_tool_results", {})
            cohort_data = last_results.get("cohort", {})
            pending_journey = last_results.get("pending_journey_confirmation", {})
            pending_cluster = last_results.get("pending_cluster_selection", {})
            pending_campaign_type = last_results.get("pending_campaign_type_selection", {})

            # Check if user is selecting a campaign type from a previous prompt
            if pending_campaign_type:
                msg_lower = message.strip().lower()
                if msg_lower.isdigit():
                    idx = int(msg_lower) - 1
                    if 0 <= idx < len(CAMPAIGN_TYPE_OPTIONS):
                        campaign_type = CAMPAIGN_TYPE_OPTIONS[idx]["id"]
                        location_name = pending_campaign_type.get("location_name")
                        zip_codes = pending_campaign_type.get("zip_codes", [])
                        logger.info(f"User selected campaign type {idx+1}: {campaign_type}")
                        # Clear pending state
                        tool_results["pending_campaign_type_selection"] = None
                    else:
                        return f"Please enter a number between 1 and {len(CAMPAIGN_TYPE_OPTIONS)}.\n\n{_format_campaign_types_for_display(pending_campaign_type.get('location_name', 'your location'))}"
                else:
                    return f"Please enter a number to select a campaign type.\n\n{_format_campaign_types_for_display(pending_campaign_type.get('location_name', 'your location'))}"

            # Check if user is selecting a cluster from a previous prompt
            elif pending_cluster:
                clusters = pending_cluster.get("clusters", [])
                location_type = pending_cluster.get("location_type")
                location_value = pending_cluster.get("location_value")
                location_label = pending_cluster.get("location_label", "")
                campaign_type = pending_cluster.get("campaign_type", "AEP_ACQUISITION")

                # Parse user's selection
                msg_lower = message.strip().lower()
                selected_cluster_id = None
                selected_cluster_label = None

                if msg_lower == "all" or "all" in msg_lower:
                    # User wants all segments - resolve without cluster filter
                    logger.info("User selected 'all' clusters")
                    selected_cluster_label = "All Segments"
                elif msg_lower.isdigit():
                    idx = int(msg_lower) - 1
                    if 0 <= idx < len(clusters):
                        selected_cluster_id = clusters[idx].get("id")
                        selected_cluster_label = clusters[idx].get("label")
                        logger.info(f"User selected cluster {idx+1}: {selected_cluster_label}")

                if selected_cluster_id or msg_lower == "all" or "all" in msg_lower:
                    # Resolve to ZIPs with the selected cluster
                    zip_codes = await _resolve_location_to_zips(
                        location_type=location_type,
                        location_value=location_value,
                        cluster_id=selected_cluster_id,
                        max_zips=10,
                    )
                    location_name = f"{location_label} - {selected_cluster_label}" if selected_cluster_label else location_label

                    # Clear pending state
                    tool_results["pending_cluster_selection"] = None
                else:
                    # Invalid selection - re-prompt
                    cluster_display = _format_clusters_for_display(clusters, location_label)
                    return f"I didn't catch that. Please enter a number (1-{len(clusters)}) or 'all'.\n\n{cluster_display}"

            else:
                # Get journey params from pending confirmation or cohort
                journey_params = pending_journey.get("params", {})
                geography = journey_params.get("geography", {})
                zip_codes = geography.get("zip_codes", [])
                campaign_type = journey_params.get("campaign_type")
                location_name = geography.get("resolved_name", cohort_data.get("name"))

                # If no params from state, extract from current message using semantic location
                if not zip_codes:
                    location_info = _extract_location_from_conversation([{"content": message}])
                    zip_codes = location_info.get("zip_codes", [])

                    # If no direct ZIPs but have semantic location, analyze geography first
                    if not zip_codes and location_info.get("location_type"):
                        loc_type = location_info["location_type"]
                        loc_value = location_info["location_value"]

                        # For broad geographies, analyze and potentially show clusters
                        if loc_type in ("state", "region", "national"):
                            logger.info(f"Analyzing geography {loc_type}={loc_value}")
                            analysis = await _analyze_geography(loc_type, loc_value)

                            if analysis.get("requires_cluster_selection") and analysis.get("clusters"):
                                # Store pending selection and return cluster menu
                                if not campaign_type:
                                    campaign_type = _extract_campaign_type(message) or "AEP_ACQUISITION"

                                tool_results["pending_cluster_selection"] = {
                                    "location_type": loc_type,
                                    "location_value": loc_value,
                                    "location_label": analysis.get("location_label", loc_value),
                                    "clusters": analysis.get("clusters", []),
                                    "campaign_type": campaign_type,
                                }

                                cluster_display = _format_clusters_for_display(
                                    analysis.get("clusters", []),
                                    analysis.get("location_label", loc_value)
                                )
                                return cluster_display

                        # For cities/ZIPs or if no clusters, resolve directly
                        logger.info(f"Resolving {loc_type}={loc_value} to ZIPs")
                        zip_codes = await _resolve_location_to_zips(
                            location_type=loc_type,
                            location_value=loc_value,
                            max_zips=10,
                        )
                        logger.info(f"Resolved to {len(zip_codes)} ZIPs: {zip_codes[:3]}")

                    # Set location name from extracted info
                    if not location_name:
                        if location_info.get("city"):
                            location_name = location_info["city"]
                        elif location_info.get("state"):
                            location_name = location_info["state"]
                        elif location_info.get("region"):
                            location_name = location_info["region"].title()
                        elif location_info.get("national"):
                            location_name = "National"

                if not campaign_type:
                    campaign_type = _extract_campaign_type(message)

                if not location_name:
                    if zip_codes:
                        location_name = f"ZIP {zip_codes[0]}"
                    else:
                        location_name = "Target Market"

                # If we have location but no campaign type, ask user to select
                if zip_codes and not campaign_type:
                    tool_results["pending_campaign_type_selection"] = {
                        "location_name": location_name,
                        "zip_codes": zip_codes,
                    }
                    return _format_campaign_types_for_display(location_name)

            # Build journey request
            journey_request = JourneyRequest(
                name=f"{location_name} {campaign_type.upper().replace('_', ' ')} Journey",
                description=f"Journey for {location_name}",
                target_cohort_id=cohort_data.get("cohort_id"),
            )

            result = await create_journey(
                request=journey_request,
                zip_codes=zip_codes if zip_codes else ["33101"],  # Fallback to Miami
            )

            # Map touchpoint type to backend channel names
            channel_map = {
                "email": "email",
                "sms": "sms",
                "mailer": "direct_mail",
                "mail": "direct_mail",
                "call": "phone_outbound",
                "phone": "phone_outbound",
                "digital_ad": "digital_ad",
                "event": "community_event",
            }

            # Store touchpoints for simulation
            touchpoints_for_simulation = [
                {
                    "id": tp.id,
                    "channel": channel_map.get(tp.type.value.lower(), tp.type.value),
                    "day": tp.day,
                    "stage": "Awareness" if tp.day < 7 else "Consideration" if tp.day < 14 else "Decision",
                }
                for tp in result.touchpoints
            ]

            tool_results["journey"] = {
                "journey_id": result.journey_id,
                "name": result.name,
                "touchpoints": len(result.touchpoints),
                "total_duration_days": result.total_duration_days,
                "estimated_total_cost": result.estimated_total_cost,
                "touchpoints_for_simulation": touchpoints_for_simulation,
            }

            touchpoint_summary = ", ".join(
                f"{tp.name} (day {tp.day})" for tp in result.touchpoints[:4]
            )

            return (
                f"Great! I've created a journey for your cohort.\n\n"
                f"**{result.name}**\n"
                f"{result.description}\n\n"
                f"**Touchpoints ({len(result.touchpoints)}):** {touchpoint_summary}\n"
                f"**Duration:** {result.total_duration_days} days\n\n"
                "Shall I simulate this journey with the cohort?"
            )
        except Exception as e:
            logger.error(f"Error creating journey: {e}")
            return f"I encountered an error creating the journey: {str(e)}. Please try again."

    # Handle journey optimization
    if intent == "optimize_journey" or "optimize" in message_lower:
        tools_used.append("optimize_journey")
        try:
            last_results = conversation_state.get("last_tool_results", {})
            journey_id = last_results.get("journey", {}).get("journey_id", "journey_default")

            result = await optimize_journey(journey_id=journey_id, optimization_goal="enrollment")

            tool_results["journey"] = {
                "journey_id": result.journey_id,
                "name": result.name,
                "touchpoints": len(result.touchpoints),
                "total_duration_days": result.total_duration_days,
                "estimated_total_cost": result.estimated_total_cost,
            }

            touchpoint_summary = ", ".join(
                f"{tp.name} (day {tp.day})" for tp in result.touchpoints[:4]
            )

            return (
                f"I've optimized the journey for maximum enrollment.\n\n"
                f"**{result.name}**\n"
                f"{result.description}\n\n"
                f"**Touchpoints ({len(result.touchpoints)}):** {touchpoint_summary}\n"
                f"**Duration:** {result.total_duration_days} days\n\n"
                "Would you like me to simulate this optimized journey?"
            )
        except Exception as e:
            logger.error(f"Error optimizing journey: {e}")
            return f"I encountered an error optimizing the journey: {str(e)}. Please try again."

    # Default: Use TerryAnn chat (full persona + knowledge base)
    # Journey creation is handled conversationally - TerryAnn gathers info, then we create
    try:
        client = get_synthwell_client()

        # Build conversation history for context
        messages = conversation_state.get("messages", [])
        conversation_history = [
            {"role": m.get("role"), "content": m.get("content")}
            for m in messages[-10:]  # Last 10 messages for context
        ] if messages else []

        # Add current message to history for param extraction
        current_messages = conversation_history + [{"role": "user", "content": message}]

        # Call TerryAnn via /chat/fast
        result = await client.chat_fast(
            message=message,
            conversation_id=conversation_state.get("conversation_id"),
        )

        tools_used.append("chat_fast")
        terryann_response = result.get("response", "")

        tool_results["chat"] = {
            "conversation_id": result.get("conversation_id"),
            "citations": result.get("citations"),
        }

        # Check if TerryAnn is ready to create a journey
        # Add her response to messages for full context
        full_conversation = current_messages + [{"role": "assistant", "content": terryann_response}]

        if _should_create_journey(terryann_response, full_conversation):
            # Extract journey params from conversation
            params = _extract_journey_params_from_conversation(full_conversation)

            if params["ready"] and (params["zip_codes"] or params["location_description"]):
                try:
                    tools_used.append("create_journey")

                    # Create the journey with extracted params
                    journey_request = JourneyRequest(name=params["name"] or "New Journey")

                    # Call full v2 pipeline (15+ data sources, Monte Carlo, Claude reasoning)
                    journey_result = await client.create_flowchart_v2(
                        zip_codes=params["zip_codes"] or ["33101"],  # Fallback if only city/state
                        campaign_type=params["campaign_type"] or "aep_acquisition",
                        name=params["name"] or "New Journey",
                        user_id=user_id,
                        created_from=surface,
                    )

                    journey_id = journey_result.get("journey_id", "unknown")
                    # v2 returns nodes instead of touchpoints
                    nodes = journey_result.get("nodes", [])
                    touchpoints = [
                        n for n in nodes if n.get("type") == "touchpoint"
                    ]

                    # Map touchpoint type to backend channel names
                    channel_map = {
                        "email": "email",
                        "sms": "sms",
                        "mailer": "direct_mail",
                        "mail": "direct_mail",
                        "call": "phone_outbound",
                        "phone": "phone_outbound",
                        "digital_ad": "digital_ad",
                        "event": "community_event",
                    }

                    # Store touchpoints for simulation
                    touchpoints_for_simulation = [
                        {
                            "id": tp.get("id", f"tp_{i}"),
                            "channel": channel_map.get(tp.get("channel", "email").lower(), tp.get("channel", "email")),
                            "day": tp.get("day", i * 7),
                            "stage": tp.get("stage", "Awareness"),
                        }
                        for i, tp in enumerate(touchpoints)
                    ]

                    tool_results["journey"] = {
                        "journey_id": journey_id,
                        "name": params["name"],
                        "zip_codes": params["zip_codes"],
                        "campaign_type": params["campaign_type"],
                        "touchpoints_count": len(touchpoints),
                        "touchpoints_for_simulation": touchpoints_for_simulation,
                    }

                    # Format touchpoint list (v2 uses 'label' for name)
                    touchpoint_list = "\n".join(
                        f"- **Day {tp.get('day', 0)}:** {tp.get('label', 'Touchpoint')} ({tp.get('channel', 'email').title()})"
                        for tp in touchpoints[:6]  # Show first 6
                    )
                    if len(touchpoints) > 6:
                        touchpoint_list += f"\n- ... and {len(touchpoints) - 6} more"

                    # Append journey creation result to TerryAnn's response
                    journey_summary = (
                        f"\n\n---\n\n"
                        f"**Journey Created:** `{journey_id}`\n\n"
                        f"**Target:** {params['location_description'] or 'Target market'}\n"
                        f"**Campaign:** {params['campaign_type'].replace('_', ' ').title()}\n\n"
                        f"**Touchpoints:**\n{touchpoint_list}\n\n"
                        f"You can now ask 'what if' questions like:\n"
                        f"- \"What if we add a mailer on day 3?\"\n"
                        f"- \"What if we remove the phone call?\""
                    )

                    return terryann_response + journey_summary

                except Exception as e:
                    logger.error(f"Error creating journey after conversation: {e}")
                    # Return TerryAnn's response even if journey creation fails
                    return terryann_response + f"\n\n(I tried to create the journey but encountered an error: {str(e)})"

        # Return TerryAnn's response as-is if not creating a journey
        return terryann_response or "I'm having trouble responding right now. Please try again."

    except SynthWellClientError as e:
        logger.error(f"Error calling TerryAnn chat: {e}")
        return (
            "I'm having trouble connecting to my knowledge base right now. "
            "In the meantime, I can help you with:\n\n"
            "- **Generate cohorts** - just say 'create a cohort for [location]'\n"
            "- **Create journeys** - tell me about your target market and campaign goals\n"
            "- **Simulate changes** - say 'what if we add a mailer on day 3?'\n"
            "- **Optimize** - say 'optimize the journey'\n\n"
            "What would you like to do?"
        )
