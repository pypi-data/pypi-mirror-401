# TerryAnn Core

Gateway + MCP Server for TerryAnn V2 - Medicare Journey Intelligence Platform.

## Overview

TerryAnn Core provides:
- **Gateway API**: Conversation endpoint that handles user messages and orchestrates responses
- **MCP Server**: Tool definitions for cohort generation, journey simulation, and campaign execution
- **Session Management**: Conversation state and context tracking

## Quick Start

```bash
# Install dependencies
pip install -e .

# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Run locally
uvicorn app.main:app --reload --port 8080
```

## API Endpoints

### Gateway

- `POST /gateway/message` - Send a message and get a response
- `GET /gateway/session/{session_id}` - Get session details
- `GET /gateway/tools` - List available MCP tools

### Health

- `GET /` - Service info
- `GET /health` - Health check

## MCP Tools

| Tool | Description |
|------|-------------|
| `generate_cohort` | Generate a cohort based on targeting criteria |
| `get_cohort` | Retrieve an existing cohort |
| `simulate_journey` | Run Monte Carlo simulation on a journey |
| `compare_scenarios` | Compare multiple journey variations |
| `create_journey` | Create a new journey blueprint |
| `modify_journey` | Modify an existing journey |
| `optimize_journey` | Auto-optimize a journey for a goal |
| `push_to_crm` | Push data to CRM (Salesforce/HubSpot) |
| `schedule_campaign` | Schedule campaign execution |

## Project Structure

```
terryann-core/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings
│   ├── gateway/             # Conversation handling
│   │   ├── router.py        # Endpoints
│   │   ├── session.py       # Session management
│   │   └── auth.py          # Auth middleware
│   ├── mcp/                 # MCP Server
│   │   ├── server.py        # Tool registration
│   │   └── tools/           # Tool implementations
│   └── models/              # Pydantic schemas
├── tests/
├── Dockerfile
├── railway.toml
└── pyproject.toml
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .
```

## Deployment

Configured for Railway deployment via `railway.toml`.

```bash
railway up
```
