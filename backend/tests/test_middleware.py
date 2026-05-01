import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from app.core.middleware import OptionsMiddleware, RequestLoggingMiddleware
from starlette.responses import JSONResponse

app = FastAPI()

# Add middlewares
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(OptionsMiddleware)

@app.get("/test")
async def dummy_endpoint():
    return {"status": "ok"}

@app.options("/test")
async def dummy_options_endpoint():
    return JSONResponse(status_code=200, content={"status": "options ok"})

client = TestClient(app)

def test_options_middleware():
    """Test that OPTIONS requests skip normal processing (handled by middleware if needed)"""
    # Note: Fastapi directly handles OPTIONS if it's explicitly defined or automatically adds it.
    response = client.options("/test")
    assert response.status_code == 200

def test_request_logging_middleware(caplog):
    """Test that standard requests are logged and have custom headers"""
    import logging
    caplog.set_level(logging.INFO)
    
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
    # Check headers
    assert "x-process-time" in response.headers
    
    # Check logs
    assert any("Request: GET /test" in record.message for record in caplog.records)
    assert any("Response: 200 - Processed in" in record.message for record in caplog.records)

def test_options_skips_logging(caplog):
    """Test that an OPTIONS request skips the logging middleware processing"""
    import logging
    caplog.set_level(logging.INFO)
    caplog.clear()

    response = client.options("/test")
    assert response.status_code == 200

    # There should be no logging records from RequestLoggingMiddleware for OPTIONS
    assert not any("Request: OPTIONS /test" in record.message for record in caplog.records)
