"""
JumpApp entrypoint.

Start with:
    pip install -r requirements.txt
    python main.py

The app root is resolved automatically from this file's location, so the app
works regardless of where the USB drive is mounted or what the directory is
named.  To override (e.g. point at a different drive), set JUMPAPP_ROOT:

    JUMPAPP_ROOT=/mnt/jumpapp/MyJumpApp python main.py

Sub-directories used at runtime (all relative to the app root):
    <root>/models    – saved model weights
    <root>/dataset   – training / evaluation data
    <root>/endpoints – optional extra endpoint modules

USB drive layout (multiple apps are supported):
    /mnt/<drive>/
        AppOne/
            jumpapp.json
            server/main.py  ← this file
            ui/index.html
            models/
            dataset/
            endpoints/
        AppTwo/
            jumpapp.json
            ...
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# ---------------------------------------------------------------------------
# Storage root
# ---------------------------------------------------------------------------

# Resolve the app root relative to this file (server/ → app root one level up).
# This makes the app location-independent — it works wherever the USB is mounted.
# Override with the JUMPAPP_ROOT env var if you need to point elsewhere.
_DEFAULT_ROOT = Path(__file__).resolve().parent.parent
JUMPAPP_ROOT  = Path(os.environ.get("JUMPAPP_ROOT", _DEFAULT_ROOT))
MODELS_DIR   = JUMPAPP_ROOT / "models"
DATASET_DIR  = JUMPAPP_ROOT / "dataset"
ENDPOINTS_DIR = JUMPAPP_ROOT / "endpoints"

# Make sure the directories exist so code can write to them without extra checks.
for _d in (MODELS_DIR, DATASET_DIR, ENDPOINTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# Allow endpoint modules stored on the USB drive to be imported directly.
if str(ENDPOINTS_DIR) not in sys.path:
    sys.path.insert(0, str(ENDPOINTS_DIR))
app = FastAPI(title="JumpApp", version="0.1.0")

# Allow the JumpApp UI (served from a local file or same origin) to reach the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class InferRequest(BaseModel):
    input: str  # replace with your actual input schema


class InferResponse(BaseModel):
    output: str  # replace with your actual output schema


# ---------------------------------------------------------------------------
# Required endpoint
# ---------------------------------------------------------------------------

@app.get("/status")
def status():
    """Returns the current health / readiness of the server."""
    return {
        "status": "ok",
        "version": "0.1.0",
        "storage": {
            "root": str(JUMPAPP_ROOT),
            "models": str(MODELS_DIR),
            "dataset": str(DATASET_DIR),
            "endpoints": str(ENDPOINTS_DIR),
        },
    }


# ---------------------------------------------------------------------------
# Optional endpoints
# ---------------------------------------------------------------------------

@app.post("/infer", response_model=InferResponse)
def infer(req: InferRequest):
    """Run inference. Replace with your model logic."""
    result = req.input  # placeholder — echo the input back
    return InferResponse(output=result)


# @app.post("/train")
# def train():
#     """Trigger a training run. Uncomment and implement if needed."""
#     return {"status": "training started"}


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
