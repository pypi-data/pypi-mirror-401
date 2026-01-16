"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .rag.router import router as rag_router
from .rag.mcp_proxy import router as mcp_proxy_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting RAG Memory web application...")
    logger.info(f"Database: {settings.DATABASE_URL}")

    # Note: Database schema is managed by Alembic migrations
    # Run `alembic upgrade head` to apply migrations
    # See backend/alembic/versions/ for migration files

    yield

    # Shutdown
    logger.info("Shutting down RAG Memory web application...")


# Create FastAPI app
app = FastAPI(
    title="RAG Memory Web",
    description="Web interface for RAG Memory knowledge base management",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
origins = settings.CORS_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(rag_router)
app.include_router(mcp_proxy_router)

logger.info("RAG Memory web application initialized")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "RAG Memory Web API",
        "version": "0.1.0",
        "docs": "/docs",
    }
