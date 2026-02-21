from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from services.ml_predictor import predict_news
from services.fact_check import fact_check_claim
from utils.decision import final_decision
from services.llm_explainer import explain_decision


# -------------------------------------------------
# FastAPI App
# -------------------------------------------------
app = FastAPI(
    title="Fake News Verification API",
    description="Hybrid AI + Fact Check + LLM Explainability System",
    version="1.0.0"
)


# -------------------------------------------------
# Health & Root Endpoints (Fixes 404)
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Fake News Verification API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# -------------------------------------------------
# Request / Response Models
# -------------------------------------------------
class NewsRequest(BaseModel):
    text: str


class NewsResponse(BaseModel):
    verdict: str
    confidence: float
    ml_label: str
    sources: List[str]
    reason: str
    explanation: str


# -------------------------------------------------
# API Endpoint
# -------------------------------------------------
@app.post("/verify", response_model=NewsResponse)
def verify_news(request: NewsRequest):

    # Step 1: ML prediction
    ml_result = predict_news(request.text)

    # Step 2: Fact check
    fact_result = fact_check_claim(request.text)

    # Step 3: Final decision logic
    decision = final_decision(ml_result, fact_result)

    # Step 4: LLM explanation
    explanation = explain_decision(
        text=request.text,
        verdict=decision["verdict"],
        ml_label=ml_result["label"],
        confidence=ml_result["confidence"],
        sources=decision.get("sources", [])
    )

    return {
        "verdict": decision["verdict"],
        "confidence": ml_result["confidence"],
        "ml_label": ml_result["label"],
        "sources": decision.get("sources", []),
        "reason": decision["reason"],
        "explanation": explanation
    }