"""Main FastAPI application for the model server proxy."""

import logging
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import chat_router

# Configure logging
log_dir = settings.log_dir
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "model_server.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Model Server Proxy",
    description="Unified proxy/gateway for multiple AI provider APIs",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "name": "Model Server Proxy",
        "version": "1.0.0",
        "status": "running",
        "providers": ["openai", "anthropic", "google"],
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


def write_pid_file():
    """Write the current process ID to the PID file."""
    pid_file = settings.pid_file
    pid_file.write_text(str(Path("/proc/self").stat().st_ino))
    logger.info(f"PID file created: {pid_file}")


def main():
    """Main entry point for the server."""
    # Write PID file for process management
    write_pid_file()

    logger.info(f"Starting Model Server Proxy on {settings.host}:{settings.port}")
    logger.info(f"Supported providers: openai, anthropic, google")

    # Run server
    uvicorn.run(
        "model_server.server:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
        access_log=True,
    )


if __name__ == "__main__":
    main()
