from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional

from database import db

app = FastAPI(title="TinderAI Backend", version="1.0.0")

# CORS setup
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" if FRONTEND_URL == "*" else FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "TinderAI backend is running"}


@app.get("/test")
async def test_db():
    if db is None:
        return {
            "backend": "ok",
            "database": "not configured",
            "connection_status": "unavailable",
            "database_url": os.getenv("DATABASE_URL"),
            "database_name": os.getenv("DATABASE_NAME"),
            "collections": []
        }
    try:
        collections = db.list_collection_names()
        return {
            "backend": "ok",
            "database": "connected",
            "connection_status": "ok",
            "database_url": os.getenv("DATABASE_URL"),
            "database_name": os.getenv("DATABASE_NAME"),
            "collections": collections,
        }
    except Exception as e:
        return {
            "backend": "ok",
            "database": "error",
            "connection_status": f"error: {e}",
            "database_url": os.getenv("DATABASE_URL"),
            "database_name": os.getenv("DATABASE_NAME"),
            "collections": []
        }
