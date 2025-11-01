"""
Main FastAPI application entrypoint.

Includes:
- CORS configuration for frontend compatibility
- API router registration
- Application metadata
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analyze import router as analyze_router
import os

# -------------------------------------------------
# Application instance
# -------------------------------------------------
app = FastAPI(
    title="inSintesi API",
    version="1.0.0",
    description="Backend service for AI-powered consensus and feedback analysis."
)

# -------------------------------------------------
# CORS Configuration
# -------------------------------------------------
# Load allowed origins from environment variable or use default localhost
allowed_origins = os.getenv("ALLOWED_ORIGINS")

if allowed_origins:
    origins = [origin.strip() for origin in allowed_origins.split(",")]
else:
    origins = [
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Routers
# -------------------------------------------------
app.include_router(analyze_router)

# -------------------------------------------------
# Root route (health check)
# -------------------------------------------------
@app.get("/", tags=["health"])
def read_root():
    """Basic health check endpoint."""
    return {"status": "ok", "message": "inSintesi API is running"}
