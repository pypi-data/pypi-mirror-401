"""Pydantic models for all tool inputs/outputs."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# --- Gateway Models ---


class MessageRequest(BaseModel):
    """Request body for /gateway/message endpoint."""

    message: str = Field(..., description="User message content")
    session_id: str | None = Field(None, description="Session ID for conversation continuity")
    surface: str = Field("cli", description="Client surface: cli, slack, web, mobile")
    context: dict[str, Any] | None = Field(None, description="Additional context for the message")


class MessageResponse(BaseModel):
    """Response from /gateway/message endpoint."""

    response: str = Field(..., description="Assistant response content")
    session_id: str = Field(..., description="Session ID for this conversation")
    tools_used: list[str] = Field(default_factory=list, description="MCP tools invoked")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional response metadata")


# --- Cohort Models ---


class CohortMember(BaseModel):
    """Individual member of a cohort."""

    id: str
    age: int
    county_fips: str
    risk_score: float
    ltv_estimate: float
    engagement_propensity: float
    preferred_channel: str


class CohortRequest(BaseModel):
    """Request to generate or retrieve a cohort."""

    county_fips: str | None = Field(None, description="Filter by county FIPS code")
    min_age: int | None = Field(None, description="Minimum age filter")
    max_age: int | None = Field(None, description="Maximum age filter")
    risk_tier: str | None = Field(None, description="Risk tier: low, medium, high")
    size: int = Field(1000, description="Target cohort size")


class CohortResponse(BaseModel):
    """Response containing cohort data."""

    cohort_id: str
    name: str
    size: int
    members: list[CohortMember]
    summary: dict[str, Any]
    created_at: datetime


# --- Simulation Models ---


class SimulationTouchpoint(BaseModel):
    """Touchpoint input for simulation."""

    id: str = Field(..., description="Touchpoint identifier")
    channel: str = Field(..., description="Channel: direct_mail, email, sms, phone_outbound, etc.")
    day: int = Field(..., description="Day in journey sequence")
    stage: str | None = Field(None, description="Journey stage (Awareness, Consideration, etc.)")


class CohortProfile(BaseModel):
    """Behavioral profile for cohort simulation."""

    effort_tolerance_score: float = Field(0.5, ge=0, le=1, description="Tolerance for effort/friction")
    confusion_susceptibility: float = Field(0.5, ge=0, le=1, description="Susceptibility to confusion")
    institutional_trust_score: float = Field(0.5, ge=0, le=1, description="Trust in institutions")
    digital_channel_score: float = Field(0.5, ge=0, le=1, description="Digital channel comfort")


class SimulationRequest(BaseModel):
    """Request to simulate journey changes (baseline vs modified)."""

    journey_id: str = Field(..., description="Journey ID")
    baseline_touchpoints: list[SimulationTouchpoint] = Field(
        ..., description="Current journey touchpoints"
    )
    modified_touchpoints: list[SimulationTouchpoint] = Field(
        ..., description="Proposed journey touchpoints"
    )
    cohort_profile: CohortProfile | None = Field(
        None, description="Optional cohort profile override"
    )


class FinalState(BaseModel):
    """Final cohort state after journey completion."""

    cumulative_fatigue: float
    trust_balance: float
    confusion_level: float


class SimulationOutput(BaseModel):
    """Results from simulating a single journey configuration."""

    total_advance_probability: float = Field(..., description="Probability of enrollment")
    total_dropout_probability: float = Field(..., description="Probability of dropout")
    journey_duration_days: int
    total_cost: float
    final_state: FinalState


class SimulationDelta(BaseModel):
    """Comparison between baseline and modified journeys."""

    advance_probability_change: float = Field(..., description="Positive = improvement")
    dropout_probability_change: float = Field(..., description="Negative = improvement")
    duration_change_days: int = Field(..., description="Negative = faster")
    cost_change: float
    interpretation: str = Field(..., description="Human-readable summary")


class SimulationResponse(BaseModel):
    """Response from journey simulation comparing baseline vs modified."""

    journey_id: str
    baseline: SimulationOutput
    modified: SimulationOutput
    delta: SimulationDelta


# --- Journey Models ---


class TouchpointType(str, Enum):
    """Types of touchpoints in a journey."""

    EMAIL = "email"
    SMS = "sms"
    MAILER = "mailer"
    CALL = "call"
    DIGITAL_AD = "digital_ad"
    EVENT = "event"


class Touchpoint(BaseModel):
    """Individual touchpoint in a journey."""

    id: str
    type: TouchpointType
    name: str
    day: int = Field(..., description="Day in journey sequence")
    content_template: str | None = None
    estimated_cost: float = 0.0
    expected_response_rate: float = 0.0


class JourneyRequest(BaseModel):
    """Request to create or modify a journey."""

    name: str = Field(..., description="Journey name")
    description: str | None = None
    touchpoints: list[Touchpoint] = Field(default_factory=list)
    target_cohort_id: str | None = None


class JourneyResponse(BaseModel):
    """Response containing journey data."""

    journey_id: str
    name: str
    description: str | None
    touchpoints: list[Touchpoint]
    total_duration_days: int
    estimated_total_cost: float
    created_at: datetime
    updated_at: datetime


# --- Execution Models ---


class CRMPushRequest(BaseModel):
    """Request to push data to CRM."""

    crm_type: str = Field(..., description="CRM system: salesforce, hubspot")
    cohort_id: str
    journey_id: str
    campaign_name: str


class CRMPushResponse(BaseModel):
    """Response from CRM push operation."""

    success: bool
    records_pushed: int
    crm_campaign_id: str | None
    errors: list[str]


class CampaignScheduleRequest(BaseModel):
    """Request to schedule a campaign."""

    journey_id: str
    cohort_id: str
    start_date: datetime
    execution_platform: str = Field(..., description="Platform: braze, salesforce, hubspot")


class CampaignScheduleResponse(BaseModel):
    """Response from campaign scheduling."""

    success: bool
    schedule_id: str | None
    start_date: datetime
    touchpoints_scheduled: int
    estimated_completion_date: datetime
    errors: list[str]
