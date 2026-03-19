import asyncio
import google.generativeai as genai
from pydantic_settings import BaseSettings
from typing import List, Dict
import os

class Settings(BaseSettings):
    google_api_key: str

    class Config:
        env_file = ".env"

# settings = Settings()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY', 'demo-key'))

model = genai.GenerativeModel('gemini-1.5-flash')

PROMPT_TEMPLATE = """
Analyze the following market data for the {sector} sector in India and generate a structured trade opportunities report.

Data:
{data}

Generate a MARKDOWN report with these sections:
# {sector} Sector - Trade Opportunities Report

## Overview
Current market summary.

## Key Trends
2-3 major trends from data.

## Trade Opportunities
Specific buy/sell/hold opportunities with reasons.

## Risks
Potential risks.

## Recommendations
Actionable advice.

Use latest data, focus on NSE/BSE stocks if mentioned. Be insightful.
"""

async def analyze_sector(sector: str, market_data: List[Dict]) -> str:
    """
    Use Gemini to generate markdown report from market data.
    """
    data_str = "\\n\\n".join([f"**{r['title']}**: {r['body']} ({r.get('href', '')})" for r in market_data])
    
    prompt = PROMPT_TEMPLATE.format(sector=sector.capitalize(), data=data_str)
    
    response = await asyncio.to_thread(model.generate_content, prompt)
    
    if response.text:
        return response.text.strip()
    else:
        raise ValueError("Gemini analysis failed")

