# Trade Opportunities API

FastAPI service that analyzes Indian market sectors for trade opportunities using Google Gemini AI and web search.

## Features
- Single endpoint: `GET /analyze/{sector}` (e.g., pharmaceuticals)
- Authentication: `Authorization: Bearer <any-key>` (guest mode)
- Rate limiting: 10/min per IP
- Returns markdown report
- In-memory sessions
- Auto docs at /docs

## Quick Setup (Windows)

1. **Navigate to project:**
   ```
   cd trade_opportunities_api
   ```

2. **Create virtual environment:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Setup .env:**
   ```
   copy .env.example .env
   ```
   - Get [Google Gemini API key](https://aistudio.google.com/app/apikey)
   - Add to .env: `GOOGLE_API_KEY=your_key`
   - `APP_SECRET_KEY=openssl rand -hex 32` (optional, generate)

5. **Run server:**
   ```
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Test endpoint:**
   ```
   curl -H "Authorization: Bearer test" http://localhost:8000/analyze/pharmaceuticals
   ```
   Or visit http://localhost:8000/docs

## Valid Sectors
pharmaceuticals, technology, agriculture (extend in code)

## Error Handling
- 401: No/Missing auth
- 422: Invalid sector
- 429: Rate limit
- 500: External API failure

## Architecture
- `data_collector.py`: DuckDuckGo search
- `analyzer.py`: Gemini analysis
- `auth.py`: Simple bearer auth
- `middleware.py`: Rate limit support

Add your Gemini key to .env and run!

