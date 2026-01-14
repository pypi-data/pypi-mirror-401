"""FastAPI application entry point for TerryAnn Core."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.gateway import router as gateway_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    settings = get_settings()
    print(f"Starting {settings.app_name} v{settings.api_version}")
    print(f"Debug mode: {settings.debug}")

    yield

    # Shutdown
    print("Shutting down TerryAnn Core")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Gateway + MCP Server for TerryAnn V2 - Medicare Journey Intelligence Platform",
        version=settings.api_version,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # Local dev
            "http://localhost:5173",  # Vite dev
            "https://*.terryann.ai",  # Production
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(gateway_router)

    @app.get("/")
    async def root():
        """Root endpoint - health check."""
        return {
            "service": settings.app_name,
            "version": settings.api_version,
            "status": "healthy",
        }

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
