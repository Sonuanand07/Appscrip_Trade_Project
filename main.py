import os
import asyncio
from fastapi import FastAPI, Depends, HTTPException, Path, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from typing import Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from auth import get_current_user
from data_collector import collect_market_data
from analyzer import analyze_sector

# In-memory session store
sessions = {}

app = FastAPI(
    title="Trade Opportunities API",
    description="FastAPI service for sector market analysis using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = Limiter(key_func=get_remote_address)

app.add_exception_handler(RateLimitExceeded, lambda request, exc: HTTPException(status_code=429, detail="Rate limit exceeded"))

@app.get("/analyze/{sector}", summary="Analyze sector for trade opportunities")
@app.state.limiter.limit("10/minute")
async def analyze_endpoint(
    request: Request,
    sector: str = Path(..., min_length=2, description="Sector name e.g. pharmaceuticals"),
    current_user: str = Depends(get_current_user)
):
    logger.info(f"Request for sector '{sector}' by user '{current_user}' from IP {get_remote_address(request)}")
    
    valid_sectors = ["pharmaceuticals", "technology", "agriculture"]
    if sector.lower() not in valid_sectors:
        raise HTTPException(status_code=422, detail=f"Valid sectors: {', '.join(valid_sectors)}")
    
    # Track session
    if current_user not in sessions:
        sessions[current_user] = {"requests": 0}
    sessions[current_user]["requests"] += 1
    
    try:
        market_data = await collect_market_data(sector)
        report = await analyze_sector(sector, market_data)
        return {"report": report, "sector": sector, "user_requests": sessions[current_user]["requests"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def docs():
    return """
    <h1>Trade Opportunities API</h1>
    <p>See <a href="/docs">/docs</a> for API docs.</p>
    <p>Example: GET /analyze/pharmaceuticals with Authorization: Bearer testkey</p>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

