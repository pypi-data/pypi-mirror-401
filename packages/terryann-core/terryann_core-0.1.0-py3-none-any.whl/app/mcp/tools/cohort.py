"""Cohort generation and retrieval tools."""

import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from app.clients.synthwell_client import SynthWellClient, SynthWellClientError, get_synthwell_client
from app.models.schemas import CohortRequest, CohortResponse, CohortMember

logger = logging.getLogger(__name__)


def extract_zip_codes(text: str) -> list[str]:
    """Extract ZIP codes from text (5-digit patterns)."""
    return re.findall(r"\b\d{5}\b", text)


def extract_location_hint(text: str) -> str | None:
    """Extract location hints from text for ZIP code lookup."""
    # Common city/location patterns
    text_lower = text.lower()
    locations = {
        "miami": ["33101", "33125", "33130", "33131", "33132"],
        "nyc": ["10001", "10002", "10003", "10004", "10005"],
        "new york": ["10001", "10002", "10003", "10004", "10005"],
        "manhattan": ["10001", "10002", "10003", "10004", "10005"],
        "brooklyn": ["11201", "11205", "11206", "11211", "11215"],
        "los angeles": ["90001", "90002", "90003", "90004", "90005"],
        "la": ["90001", "90002", "90003", "90004", "90005"],
        "chicago": ["60601", "60602", "60603", "60604", "60605"],
        "houston": ["77001", "77002", "77003", "77004", "77005"],
        "phoenix": ["85001", "85002", "85003", "85004", "85005"],
        "dallas": ["75201", "75202", "75203", "75204", "75205"],
        "san diego": ["92101", "92102", "92103", "92104", "92105"],
        "tampa": ["33601", "33602", "33603", "33604", "33605"],
        "orlando": ["32801", "32802", "32803", "32804", "32805"],
    }

    for location, zips in locations.items():
        if location in text_lower:
            return zips[0]  # Return first ZIP for the location

    return None


async def generate_cohort(
    request: CohortRequest,
    message: str | None = None,
    client: SynthWellClient | None = None,
) -> CohortResponse:
    """
    Generate a cohort based on targeting criteria.

    Calls the SynthWell backend to create a journey with cohort parameters,
    then extracts cohort information from the response.

    Args:
        request: Cohort request with filtering criteria
        message: Optional original user message for ZIP extraction
        client: Optional SynthWell client (for testing)
    """
    client = client or get_synthwell_client()

    # Extract ZIP codes from request or message
    zip_codes = []

    if message:
        # Try to extract ZIP codes from the message
        zip_codes = extract_zip_codes(message)

        # If no explicit ZIPs, try to infer from location
        if not zip_codes:
            location_zip = extract_location_hint(message)
            if location_zip:
                zip_codes = [location_zip]

    # Fall back to county FIPS if we have it (convert to sample ZIP)
    if not zip_codes and request.county_fips:
        # Use county FIPS as a hint - in reality we'd look up ZIPs
        zip_codes = [request.county_fips[:5].zfill(5)]

    # Default to sample ZIPs if nothing found
    if not zip_codes:
        zip_codes = ["33101"]  # Default to Miami

    try:
        # Call SynthWell backend
        result = await client.create_journey(
            zip_codes=zip_codes,
            name=f"Cohort for {', '.join(zip_codes)}",
            campaign_type="aep_acquisition",
        )

        # Extract cohort info from journey response
        journey_data = result.get("journey", result)
        cohort_data = journey_data.get("cohort", {})

        # Build cohort response from backend data
        cohort_id = cohort_data.get("id", f"cohort_{uuid.uuid4().hex[:8]}")
        cohort_size = cohort_data.get("size", request.size)

        # Map backend members to our schema (if available)
        members = []
        for member_data in cohort_data.get("members", [])[:10]:
            members.append(
                CohortMember(
                    id=member_data.get("id", f"member_{uuid.uuid4().hex[:8]}"),
                    age=member_data.get("age", 70),
                    county_fips=member_data.get("county_fips", request.county_fips or "unknown"),
                    risk_score=member_data.get("risk_score", 0.5),
                    ltv_estimate=member_data.get("ltv_estimate", 3000.0),
                    engagement_propensity=member_data.get("engagement_propensity", 0.6),
                    preferred_channel=member_data.get("preferred_channel", "email"),
                )
            )

        return CohortResponse(
            cohort_id=cohort_id,
            name=cohort_data.get("name", f"Cohort for {', '.join(zip_codes)}"),
            size=cohort_size,
            members=members,
            summary=cohort_data.get("summary", {
                "avg_age": 72,
                "avg_risk_score": 0.45,
                "avg_ltv": 3200.0,
                "channel_distribution": {
                    "email": 0.45,
                    "sms": 0.30,
                    "mailer": 0.25,
                },
                "zip_codes": zip_codes,
            }),
            created_at=datetime.now(timezone.utc),
        )

    except SynthWellClientError as e:
        logger.warning(f"SynthWell API error, falling back to mock: {e}")
        # Fall back to mock response on error
        return await _generate_mock_cohort(request)


async def get_cohort(
    cohort_id: str,
    client: SynthWellClient | None = None,
) -> CohortResponse | None:
    """
    Retrieve an existing cohort by ID.

    Currently returns mock data - cohort persistence coming later.
    """
    # TODO: Wire to backend cohort retrieval when available
    return CohortResponse(
        cohort_id=cohort_id,
        name=f"Retrieved Cohort {cohort_id}",
        size=1500,
        members=[],
        summary={
            "avg_age": 71,
            "avg_risk_score": 0.42,
            "avg_ltv": 3100.0,
            "channel_distribution": {
                "email": 0.40,
                "sms": 0.35,
                "mailer": 0.25,
            },
        },
        created_at=datetime.now(timezone.utc),
    )


async def _generate_mock_cohort(request: CohortRequest) -> CohortResponse:
    """Generate mock cohort data as fallback."""
    members = []
    for i in range(min(request.size, 10)):
        members.append(
            CohortMember(
                id=f"member_{uuid.uuid4().hex[:8]}",
                age=65 + (i % 20),
                county_fips=request.county_fips or "36061",
                risk_score=0.3 + (i * 0.05),
                ltv_estimate=2500.0 + (i * 100),
                engagement_propensity=0.6 + (i * 0.02),
                preferred_channel=["email", "sms", "mailer"][i % 3],
            )
        )

    return CohortResponse(
        cohort_id=f"cohort_{uuid.uuid4().hex[:8]}",
        name=f"Generated Cohort - {request.county_fips or 'All Counties'}",
        size=request.size,
        members=members,
        summary={
            "avg_age": 72,
            "avg_risk_score": 0.45,
            "avg_ltv": 3200.0,
            "channel_distribution": {
                "email": 0.45,
                "sms": 0.30,
                "mailer": 0.25,
            },
        },
        created_at=datetime.now(timezone.utc),
    )
