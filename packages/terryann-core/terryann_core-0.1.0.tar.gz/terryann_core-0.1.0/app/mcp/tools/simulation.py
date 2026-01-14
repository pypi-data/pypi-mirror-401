"""Journey simulation tools using SynthWell /journey/{id}/simulate endpoint."""

import logging
from typing import Any

from app.clients.synthwell_client import SynthWellClient, get_synthwell_client
from app.models.schemas import (
    SimulationRequest,
    SimulationResponse,
    SimulationOutput,
    SimulationDelta,
    FinalState,
    SimulationTouchpoint,
    CohortProfile,
)

logger = logging.getLogger(__name__)


async def simulate_journey_changes(
    journey_id: str,
    baseline_touchpoints: list[dict[str, Any]],
    modified_touchpoints: list[dict[str, Any]],
    cohort_profile: dict[str, Any] | None = None,
    client: SynthWellClient | None = None,
) -> SimulationResponse:
    """
    Simulate the impact of journey changes using the physics engine.

    Compares baseline touchpoints against modified touchpoints to show
    the impact of proposed changes (e.g., "what if we add a mailer?").

    Args:
        journey_id: Journey ID (used to load stored cohort profile if not provided)
        baseline_touchpoints: Current journey state (list of dicts with id, channel, day, stage)
        modified_touchpoints: Proposed changes (same structure)
        cohort_profile: Optional cohort behavioral profile override
        client: Optional SynthWell client (for testing)

    Returns:
        SimulationResponse with baseline, modified, and delta comparison

    Raises:
        SynthWellClientError: If the backend request fails
    """
    client = client or get_synthwell_client()

    # Call the backend simulation endpoint
    result = await client.simulate_journey(
        journey_id=journey_id,
        baseline_touchpoints=baseline_touchpoints,
        modified_touchpoints=modified_touchpoints,
        cohort_profile=cohort_profile,
    )

    # Parse the response into our schema
    baseline_data = result.get("baseline", {})
    modified_data = result.get("modified", {})
    delta_data = result.get("delta", {})

    baseline = SimulationOutput(
        total_advance_probability=baseline_data.get("total_advance_probability", 0.0),
        total_dropout_probability=baseline_data.get("total_dropout_probability", 0.0),
        journey_duration_days=baseline_data.get("journey_duration_days", 0),
        total_cost=baseline_data.get("total_cost", 0.0),
        final_state=FinalState(
            cumulative_fatigue=baseline_data.get("final_state", {}).get("cumulative_fatigue", 0.0),
            trust_balance=baseline_data.get("final_state", {}).get("trust_balance", 0.0),
            confusion_level=baseline_data.get("final_state", {}).get("confusion_level", 0.0),
        ),
    )

    modified = SimulationOutput(
        total_advance_probability=modified_data.get("total_advance_probability", 0.0),
        total_dropout_probability=modified_data.get("total_dropout_probability", 0.0),
        journey_duration_days=modified_data.get("journey_duration_days", 0),
        total_cost=modified_data.get("total_cost", 0.0),
        final_state=FinalState(
            cumulative_fatigue=modified_data.get("final_state", {}).get("cumulative_fatigue", 0.0),
            trust_balance=modified_data.get("final_state", {}).get("trust_balance", 0.0),
            confusion_level=modified_data.get("final_state", {}).get("confusion_level", 0.0),
        ),
    )

    delta = SimulationDelta(
        advance_probability_change=delta_data.get("advance_probability_change", 0.0),
        dropout_probability_change=delta_data.get("dropout_probability_change", 0.0),
        duration_change_days=delta_data.get("duration_change_days", 0),
        cost_change=delta_data.get("cost_change", 0.0),
        interpretation=delta_data.get("interpretation", ""),
    )

    return SimulationResponse(
        journey_id=journey_id,
        baseline=baseline,
        modified=modified,
        delta=delta,
    )


def create_modified_touchpoints(
    baseline: list[dict[str, Any]],
    add: list[dict[str, Any]] | None = None,
    remove_ids: list[str] | None = None,
    update: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """
    Helper to create modified touchpoints from baseline + changes.

    Args:
        baseline: Current touchpoints
        add: Touchpoints to add
        remove_ids: IDs of touchpoints to remove
        update: Dict of {touchpoint_id: {fields to update}}

    Returns:
        Modified touchpoint list

    Example:
        # Add a mailer on day 2
        modified = create_modified_touchpoints(
            baseline=current_touchpoints,
            add=[{"id": "new_mailer", "channel": "direct_mail", "day": 2}]
        )

        # Remove a touchpoint
        modified = create_modified_touchpoints(
            baseline=current_touchpoints,
            remove_ids=["tp_to_remove"]
        )

        # Change a touchpoint's channel
        modified = create_modified_touchpoints(
            baseline=current_touchpoints,
            update={"tp_1": {"channel": "sms"}}
        )
    """
    import copy

    # Start with a copy of baseline
    result = copy.deepcopy(baseline)

    # Remove touchpoints
    if remove_ids:
        result = [tp for tp in result if tp.get("id") not in remove_ids]

    # Update touchpoints
    if update:
        for tp in result:
            tp_id = tp.get("id")
            if tp_id in update:
                tp.update(update[tp_id])

    # Add new touchpoints
    if add:
        result.extend(add)

    # Sort by day
    result.sort(key=lambda tp: tp.get("day", 0))

    return result
