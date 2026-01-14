"""Main FastAPI application."""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.utils.config import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Chatbot Penetration Testing Framework",
    description="Automated adversarial testing for AI chatbots",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Prometheus Metrics
try:
    from prometheus_fastapi_instrumentator import Instrumentator

    # Instrument FastAPI app with Prometheus metrics
    Instrumentator().instrument(app).expose(
        app, endpoint="/metrics", include_in_schema=False  # Don't show in OpenAPI docs
    )
    logger.info("prometheus_enabled", endpoint="/metrics")
except ImportError:
    logger.warning("prometheus_disabled", reason="prometheus-fastapi-instrumentator not installed")
except Exception as e:
    logger.warning("prometheus_setup_failed", error=str(e))

# CORS Middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "AI Chatbot Penetration Testing Framework",
        "version": "1.0.0",
        "environment": settings.environment,
        "dashboard": "/dashboard",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.environment}


# Include routers
from src.api.routes import websocket, reports

app.include_router(websocket.router, prefix="/api/v1/ws")
app.include_router(reports.router)

# Serve dashboard
FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend"


@app.get("/dashboard")
async def serve_dashboard():
    """Serve the real-time dashboard."""
    dashboard_path = FRONTEND_DIR / "dashboard.html"
    if dashboard_path.exists():
        return FileResponse(dashboard_path, media_type="text/html")
    return JSONResponse(status_code=404, content={"error": "Dashboard not found"})


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        exc_info=True,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.is_development else "An error occurred",
        },
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("application_starting", environment=settings.environment, port=settings.api_port)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("application_shutting_down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
    )
