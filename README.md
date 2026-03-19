# Appscrip Trade Opportunities API 🎯

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-black?logo=fastapi)](https://fastapi.tiangolo.com)
[![Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI-blue)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**FastAPI service analyzing Indian market sectors (pharma, tech, agriculture) for trade opportunities using Google Gemini AI & real-time web data (NSE/BSE).**

## ✨ Features
- Single endpoint: `GET /analyze/{sector}`
- **AI reports**: Structured markdown via Gemini 1.5 Flash
- **Live data**: DuckDuckGo search for latest market news
- **Security**: Bearer auth, rate limit (10/min), validation
- **Sessions**: In-memory request tracking per user
- **Async**: Full non-blocking workflow
- **Docs**: `/docs` Swagger UI

## 🚀 Quick Start (Windows/Linux/Mac)
```bash
cd trade_opportunities_api
python -
