from duckduckgo_search import AsyncDDGS
import asyncio
from typing import List

async def collect_market_data(sector: str) -> List[dict]:
    """
    Collect current market news and data for sector in India using DuckDuckGo.
    """
    async with AsyncDDGS() as ddgs:
        query = f'"{sector}" sector India stock market news opportunities NSE BSE latest'
        results = []
        
        # Text search
        async for result in ddgs.text(query, max_results=10):
            results.append({
                "title": result.get("title", ""),
                "body": result.get("body", ""),
                "href": result.get("href", "")
            })
        
        # News search
        async for result in ddgs.news(query, max_results=10):
            results.append({
                "title": result.get("title", ""),
                "body": result.get("snippet", ""),
                "href": result.get("url", "")
            })
        
        return results[:15]  # Limit total

