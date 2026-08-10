from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from aetheropt.api.router import api_router
from aetheropt.db.base import Base
from aetheropt.db.session import engine
from aetheropt.config import settings

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AetherOpt API",
    description="Production-grade Quantum-Inspired Optimization Platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# Optional frontend serving
import os
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Simple HTMX/Alpine UI or instructions
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r") as f:
            return f.read()
    return "<h1>AetherOpt is running</h1><p>API is at <a href='/docs'>/docs</a></p>"

def start():
    """Entry point for the CLI script."""
    import uvicorn
    uvicorn.run("aetheropt.main:app", host="127.0.0.1", port=8000, reload=True)
