"""
AIDiscuss FastAPI Backend
Main application server
"""

import logging
import signal
import webbrowser
from contextlib import asynccontextmanager
from pathlib import Path
from importlib.resources import files

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from aidiscuss.app.routers import (
    chat,
    health,
    providers,
    agents,
    rag,
    rag_control,
    memory,
    quality,
    tools,
    analytics,
    offline,
    keys,
    sync,
    conversations,
    provider_keys,
    export,
    chat_config,
    admin_override,
)
from aidiscuss.app.routers import settings as settings_router
from aidiscuss.app.core.config import settings
from aidiscuss.app.core.port_manager import get_server_port
from aidiscuss.app.db.base import init_db
from aidiscuss import __version__

logger = logging.getLogger("aidiscuss.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Initializing AIDiscuss backend...")
    logger.info(f"Database: {settings.DATABASE_URL}")

    # Initialize database
    await init_db()
    logger.info("Database initialized successfully")

    yield

    # Shutdown
    logger.info("Shutting down AIDiscuss backend...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="AIDiscuss API",
    description="Backend API for AIDiscuss multi-agent conversational AI",
    version=__version__,
    lifespan=lifespan,
)

# CORS middleware - use settings for allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler for unhandled errors"""
    logger.exception(f"Unhandled exception on {request.url.path}", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error. Check logs for details.",
            "path": str(request.url.path),
        },
    )

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(providers.router, prefix="/api/providers", tags=["providers"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(rag.router, prefix="/api/rag", tags=["rag"])
app.include_router(rag_control.router, prefix="/api/rag/control", tags=["rag-control"])
app.include_router(memory.router, prefix="/api", tags=["memory"])
app.include_router(quality.router, prefix="/api", tags=["quality"])
app.include_router(tools.router, prefix="/api", tags=["tools"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])
app.include_router(offline.router, prefix="/api", tags=["offline"])
app.include_router(keys.router, prefix="/api/keys", tags=["keys"])
app.include_router(provider_keys.router, prefix="/api/provider-keys", tags=["provider-keys"])
app.include_router(sync.router, prefix="/api", tags=["sync"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
app.include_router(settings_router.router, prefix="/api/settings", tags=["settings"])
app.include_router(export.router, tags=["export"])
app.include_router(chat_config.router, tags=["chat-config"])
app.include_router(admin_override.router, tags=["admin"])

# Serve static files (React app) from package data
def get_dist_path() -> Path | None:
    """
    Get path to frontend dist directory using package resource loading.

    Returns:
        Path to dist directory if found, None otherwise.
    """
    try:
        # Try importlib.resources (Python 3.9+) for installed package
        import aidiscuss
        dist_path = files(aidiscuss) / "dist"
        # Convert to Path and check if it exists
        dist_path_obj = Path(str(dist_path))
        if dist_path_obj.exists() and dist_path_obj.is_dir():
            return dist_path_obj
    except (ImportError, TypeError, AttributeError):
        pass

    # Fallback for development (editable install)
    dev_dist_path = Path(__file__).parent.parent / "dist"
    if dev_dist_path.exists() and dev_dist_path.is_dir():
        return dev_dist_path

    logger.warning("Frontend dist directory not found - UI will not be available")
    return None


dist_path = get_dist_path()
if dist_path:
    logger.info(f"Serving frontend from: {dist_path}")
    # Mount static assets
    app.mount("/assets", StaticFiles(directory=str(dist_path / "assets")), name="assets")

    # SPA Fallback Middleware - serves index.html for 404s on non-API routes
    class SPAStaticFilesMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            response = await call_next(request)

            # If it's a 404 and NOT an API route and it's a GET request, serve index.html
            if (
                response.status_code == 404
                and not request.url.path.startswith("/api")
                and request.method == "GET"
            ):
                index_path = dist_path / "index.html"
                if index_path.exists():
                    return FileResponse(str(index_path))

            return response

    app.add_middleware(SPAStaticFilesMiddleware)


async def run_server() -> None:
    """
    Run the AIDiscuss FastAPI server.

    Called from CLI entry point (aidiscuss.cli:main).
    Handles port discovery, browser opening, and graceful shutdown.
    """
    import threading
    import atexit
    import sys
    import os

    # Discover available port
    port = get_server_port(preferred_port=settings.PORT, host=settings.HOST)
    server_url = f"http://{settings.HOST}:{port}"

    logger.info(f"Starting server on {server_url}")

    # Auto-open browser in a daemon thread
    def open_browser():
        import time
        time.sleep(1.5)  # Wait for server to start
        try:
            webbrowser.open(server_url)
            logger.info("Browser opened successfully")
        except Exception as e:
            logger.warning(f"Could not open browser: {e}")

    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Configure uvicorn
    config = uvicorn.Config(
        app,  # Use app instance directly
        host=settings.HOST,
        port=port,
        log_level="info",
        timeout_graceful_shutdown=5,
    )
    server = uvicorn.Server(config)

    # Handle signals properly
    def signal_handler(signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, initiating shutdown...")
        server.should_exit = True

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    if hasattr(signal, 'SIGBREAK'):  # Windows
        signal.signal(signal.SIGBREAK, signal_handler)

    # Run server
    try:
        await server.serve()
    except Exception as e:
        logger.exception(f"Server error: {e}")
        raise
    finally:
        logger.info("Server stopped")

        # Force exit on Windows after graceful shutdown completes
        # This is necessary due to known uvicorn/asyncio hanging issues on Windows
        # See: https://github.com/encode/uvicorn/discussions/2327
        if sys.platform == "win32":
            # Give a brief moment for any final cleanup
            import time
            time.sleep(0.1)
            os._exit(0)
