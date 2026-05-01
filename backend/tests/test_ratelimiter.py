import pytest
import asyncio
from fastapi import Request
from app.core.ratelimiter import RateLimiter, RateLimitConfig

@pytest.mark.asyncio
async def test_ratelimiter_initialization_fallback():
    """Unit test: Ratelimiter should fallback to memory if Redis fails/is not used in Test env."""
    limiter_instance = RateLimiter()
    
    # We purposefully don't provide a valid Redis or we let it fail fast if not connected
    await limiter_instance.initialize()
    
    # Check that it's initialized
    assert limiter_instance._initialized is True
    assert getattr(limiter_instance, '_limiter') is not None
    
    # Cleanup
    await limiter_instance.close()

def test_rate_limit_config_by_endpoint():
    """Unit test: Dynamics rate limit rules based on endpoints"""
    class MockRequest:
        def __init__(self, path):
            self.url = type('URL', (), {'path': path})()
            
    # Auth path
    req_auth = MockRequest("/api/v1/auth/login")
    assert "per" in RateLimitConfig.by_endpoint(req_auth)
    
    # Write operations
    req_write = MockRequest("/api/v1/places/create")
    assert RateLimitConfig.by_endpoint(req_write) == RateLimitConfig.WRITE
    
    # Analysis operations
    req_analysis = MockRequest("/api/v1/analysis/insight")
    assert RateLimitConfig.by_endpoint(req_analysis) == RateLimitConfig.ANALYSIS
    
    # General (fallback)
    req_general = MockRequest("/api/v1/health")
    assert RateLimitConfig.by_endpoint(req_general) == RateLimitConfig.GENERAL
