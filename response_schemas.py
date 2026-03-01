from pydantic import BaseModel
from typing import Dict, Any, Optional

class AnalyzeResponse(BaseModel):
    organization_profile: Dict[str, Any]
    asset_inventory: Dict[str, Any]
    threat_scenarios: Dict[str, Any]
    attack_simulations: Dict[str, Any]
    fair_risk_analysis: Dict[str, Any]
    qualitative_risk: Dict[str, Any]
    recommended_controls: Dict[str, Any]
    prioritized_risks: Dict[str, Any]
    risk_report: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    timestamp: float
    version: str
    message: str

class AgentStatusResponse(BaseModel):
    agents: Dict[str, str]
    rag_status: Dict[str, str]
    overall_status: str
