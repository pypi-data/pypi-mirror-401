"""MCP Server setup and tool registration."""

from typing import Any, Callable
from app.mcp.tools import (
    generate_cohort,
    get_cohort,
    simulate_journey_changes,
    create_modified_touchpoints,
    create_journey,
    modify_journey,
    optimize_journey,
    push_to_crm,
    schedule_campaign,
)


class MCPServer:
    """
    MCP Server for TerryAnn intelligence operations.

    Exposes tools that can be called by Claude during conversations
    to perform cohort generation, journey simulation, and campaign execution.
    """

    def __init__(self):
        self.tools: dict[str, Callable] = {}
        self._register_tools()

    def _register_tools(self):
        """Register all available MCP tools."""
        self.tools = {
            # Cohort tools
            "generate_cohort": generate_cohort,
            "get_cohort": get_cohort,
            # Simulation tools
            "simulate_journey_changes": simulate_journey_changes,
            # Journey tools
            "create_journey": create_journey,
            "modify_journey": modify_journey,
            "optimize_journey": optimize_journey,
            # Execution tools
            "push_to_crm": push_to_crm,
            "schedule_campaign": schedule_campaign,
        }

    def list_tools(self) -> list[dict[str, Any]]:
        """Return list of available tools with their schemas."""
        return [
            {
                "name": "generate_cohort",
                "description": "Generate a cohort based on targeting criteria (county, age, risk tier)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "county_fips": {"type": "string", "description": "Filter by county FIPS code"},
                        "min_age": {"type": "integer", "description": "Minimum age filter"},
                        "max_age": {"type": "integer", "description": "Maximum age filter"},
                        "risk_tier": {"type": "string", "enum": ["low", "medium", "high"]},
                        "size": {"type": "integer", "description": "Target cohort size", "default": 1000},
                    },
                },
            },
            {
                "name": "get_cohort",
                "description": "Retrieve an existing cohort by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cohort_id": {"type": "string", "description": "Cohort ID to retrieve"},
                    },
                    "required": ["cohort_id"],
                },
            },
            {
                "name": "simulate_journey_changes",
                "description": "Simulate the impact of journey changes. Compare baseline touchpoints against modified touchpoints to see the impact of proposed changes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "journey_id": {"type": "string", "description": "Journey ID"},
                        "baseline_touchpoints": {
                            "type": "array",
                            "items": {"type": "object"},
                            "description": "Current journey touchpoints (id, channel, day, stage)",
                        },
                        "modified_touchpoints": {
                            "type": "array",
                            "items": {"type": "object"},
                            "description": "Proposed journey touchpoints",
                        },
                        "cohort_profile": {
                            "type": "object",
                            "description": "Optional cohort behavioral profile override",
                        },
                    },
                    "required": ["journey_id", "baseline_touchpoints", "modified_touchpoints"],
                },
            },
            {
                "name": "create_journey",
                "description": "Create a new journey blueprint",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Journey name"},
                        "description": {"type": "string"},
                        "touchpoints": {"type": "array", "items": {"type": "object"}},
                        "target_cohort_id": {"type": "string"},
                    },
                    "required": ["name"],
                },
            },
            {
                "name": "modify_journey",
                "description": "Modify an existing journey (add/remove/move touchpoints)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "journey_id": {"type": "string"},
                        "modifications": {"type": "object"},
                    },
                    "required": ["journey_id", "modifications"],
                },
            },
            {
                "name": "optimize_journey",
                "description": "Automatically optimize a journey for a specific goal",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "journey_id": {"type": "string"},
                        "optimization_goal": {
                            "type": "string",
                            "enum": ["enrollment", "cost", "engagement", "retention"],
                            "default": "enrollment",
                        },
                    },
                    "required": ["journey_id"],
                },
            },
            {
                "name": "push_to_crm",
                "description": "Push cohort and journey data to a CRM system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "crm_type": {"type": "string", "enum": ["salesforce", "hubspot"]},
                        "cohort_id": {"type": "string"},
                        "journey_id": {"type": "string"},
                        "campaign_name": {"type": "string"},
                    },
                    "required": ["crm_type", "cohort_id", "journey_id", "campaign_name"],
                },
            },
            {
                "name": "schedule_campaign",
                "description": "Schedule a campaign for execution on a marketing platform",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "journey_id": {"type": "string"},
                        "cohort_id": {"type": "string"},
                        "start_date": {"type": "string", "format": "date-time"},
                        "execution_platform": {"type": "string", "enum": ["braze", "salesforce", "hubspot"]},
                    },
                    "required": ["journey_id", "cohort_id", "start_date", "execution_platform"],
                },
            },
        ]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Execute a tool by name with given arguments."""
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")

        tool_fn = self.tools[name]
        return await tool_fn(**arguments)
