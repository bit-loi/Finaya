from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging
import os

from app.core.config import settings
from app.core.database import init_db
from app.core.dependencies import container
from app.core.ratelimiter import rate_limiter, rate_limit_exceeded_handler  
from app.api.v1.auth import router as auth_router
from app.api.v1.analysis import router as analysis_router
from app.core.middleware import OptionsMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger = logging.getLogger(__name__)
    logger.info(" Starting Finaya Backend...")

    # Initialize rate limiter first
    try:
        await rate_limiter.initialize()
        app.state.limiter = rate_limiter.limiter
        app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
        logger.info("Rate limiter initialized and added to app state")
    except Exception as e:
        logger.error(f"❌ Failed to initialize rate limiter: {e}")
        # raise # Allow startup to continue

    # Initialize dependency container
    try:
        await container.initialize()
        logger.info("Dependency container initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize dependency container: {e}")
        # raise # Allow startup to continue

    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"Database init failed: {e}")

    logger.info("All services initialized successfully")

    yield  # <---- app runs here

    # Graceful shutdown
    logger.info("Shutting down Finaya Backend...")
    try:
        await container.close()
        await rate_limiter.close()
        logger.info("Services shut down gracefully")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")

# Create FastAPI application
app = FastAPI(
    title="Finaya API",
    description="AI-Powered Business Location Analysis Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Middleware Configuration
# FastAPI add_middleware adds to the TOP of the stack (reverse order of addition).
# To make CORSMiddleware the outermost middleware (running first for requests, last for responses),
# it must be added last. This ensures preflight OPTIONS requests are handled correctly.

# 1. Add SlowAPI Middleware
app.add_middleware(SlowAPIMiddleware)

# 2. OPTIONS Middleware - Skip/pass processing for OPTIONS requests
# Added before CORSMiddleware so CORSMiddleware wraps it
app.add_middleware(OptionsMiddleware)

# 3. CORS Configuration - Added LAST so it runs FIRST (outermost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # ✅ Use parsed list from settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Finaya API",
        "version": "1.0.0"
    }

from app.api.v1.agent import router as agent_router
from app.api.v1.places import router as places_router

# API Routes
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(analysis_router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(agent_router, prefix="/api/v1/agent", tags=["AI Agent"])
app.include_router(places_router, prefix="/api/v1/places", tags=["Places"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Finaya API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("FINAYA_BIND_HOST", "127.0.0.1"),
        port=8000,
        reload=True,
        log_level="info"
    )
