"""
Cyber Risk Analysis and Threat Modeling Platform
FastAPI Backend - Main Application
"""

import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from schemas.request_schemas import AnalyzeRequest
from schemas.response_schemas import AnalyzeResponse, HealthResponse, AgentStatusResponse
from agents.orchestrator import OrchestratorAgent

app = FastAPI(
    title="Cyber Risk Analysis Platform",
    description="AI-powered Cyber Risk Analysis and Threat Modeling for SMEs using FAIR methodology",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS - allow all origins for Base44 frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = OrchestratorAgent()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        version="1.0.0",
        message="Cyber Risk Analysis Platform is running"
    )

@app.get("/agents/status", response_model=AgentStatusResponse)
async def agents_status():
    return AgentStatusResponse(
        agents={
            "organization_profiler": "ready",
            "asset_inference": "ready",
            "threat_intelligence": "ready",
            "threat_modeling_simulation": "ready",
            "fair_risk_calculation": "ready",
            "qualitative_risk_analysis": "ready",
            "control_recommendation": "ready",
            "risk_prioritization": "ready",
            "report_generation": "ready",
            "orchestrator": "ready",
        },
        rag_status={
            "vector_store": "ready",
            "structured_retrieval": "ready",
            "embeddings": "ready",
        },
        overall_status="all_systems_operational"
    )

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    if not request.organization_description or len(request.organization_description.strip()) < 10:
        raise HTTPException(status_code=400, detail="Organization description must be at least 10 characters.")
    try:
        result = await orchestrator.run(request.organization_description)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
