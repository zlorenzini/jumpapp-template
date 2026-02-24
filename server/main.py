"""
JumpApp entrypoint.

Start with:
    pip install -r requirements.txt
    python main.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

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
    return {"status": "ok", "version": "0.1.0"}


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
