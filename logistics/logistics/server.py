from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline import EthosPipeline

app = FastAPI()

# create pipeline ONCE
pipeline = EthosPipeline()

class EthosRequest(BaseModel):
    description: str

@app.post("/ai/analyze")
def analyze(req: EthosRequest):
    """
    Trigger the same pipeline that CLI uses,
    but via HTTP instead of stdin / argv
    """
    decision = pipeline.process(req.description)

    # convert decision object to JSON
    return {
        "priority_level": decision.priority_level,
        "requires_approval": decision.requires_approval,
        "explanation": decision.explanation,
        "score": decision.score
    }