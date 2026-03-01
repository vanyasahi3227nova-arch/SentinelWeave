"""
Agent 10: Orchestrator Agent
Coordinates all agents in sequence and aggregates outputs.
"""

import asyncio
from typing import Dict, Any

from agents.organization_profiler import OrganizationProfilerAgent
from agents.asset_inference import AssetInferenceAgent
from agents.threat_intelligence import ThreatIntelligenceAgent
from agents.threat_modeling_simulation import ThreatModelingSimulationAgent
from agents.fair_risk_calculation import FAIRRiskCalculationAgent
from agents.qualitative_risk_analysis import QualitativeRiskAnalysisAgent
from agents.control_recommendation import ControlRecommendationAgent
from agents.risk_prioritization import RiskPrioritizationAgent
from agents.report_generation import ReportGenerationAgent
from rag.hybrid_rag import rag


class OrchestratorAgent:
    """
    Coordinates the full analysis pipeline:
    User Input → Organization Profiler → Asset Inference → Threat Intelligence
    → Threat Simulation → FAIR Risk Calculation → Qualitative Analysis
    → Control Recommendation → Prioritization → Report Generation
    """

    def __init__(self):
        # Initialize RAG on startup
        rag.initialize()

        self.profiler = OrganizationProfilerAgent()
        self.asset_agent = AssetInferenceAgent()
        self.threat_agent = ThreatIntelligenceAgent()
        self.simulation_agent = ThreatModelingSimulationAgent()
        self.fair_agent = FAIRRiskCalculationAgent()
        self.qualitative_agent = QualitativeRiskAnalysisAgent()
        self.control_agent = ControlRecommendationAgent()
        self.prioritization_agent = RiskPrioritizationAgent()
        self.report_agent = ReportGenerationAgent()

    async def run(self, organization_description: str) -> Dict[str, Any]:
        """
        Execute full analysis pipeline asynchronously.
        Returns complete structured risk analysis.
        """

        # Run synchronous agents in thread pool to avoid blocking
        loop = asyncio.get_event_loop()

        # Agent 1: Organization Profiling
        org_profile = await loop.run_in_executor(
            None, self.profiler.run, organization_description
        )

        # Agent 2: Asset Inference
        asset_inventory = await loop.run_in_executor(
            None, self.asset_agent.run, org_profile
        )

        # Agent 3: Threat Intelligence
        threat_scenarios = await loop.run_in_executor(
            None, self.threat_agent.run, org_profile, asset_inventory
        )

        # Agent 4: Threat Modeling Simulation
        attack_simulations = await loop.run_in_executor(
            None, self.simulation_agent.run, threat_scenarios, asset_inventory
        )

        # Agent 5: FAIR Risk Calculation
        fair_risk_analysis = await loop.run_in_executor(
            None, self.fair_agent.run, org_profile, asset_inventory, threat_scenarios
        )

        # Agent 6: Qualitative Risk Analysis
        qualitative_risk = await loop.run_in_executor(
            None, self.qualitative_agent.run, fair_risk_analysis, org_profile
        )

        # Agent 7: Control Recommendation
        recommended_controls = await loop.run_in_executor(
            None, self.control_agent.run, threat_scenarios, fair_risk_analysis, org_profile
        )

        # Agent 8: Risk Prioritization
        prioritized_risks = await loop.run_in_executor(
            None, self.prioritization_agent.run, fair_risk_analysis, qualitative_risk, recommended_controls
        )

        # Agent 9: Report Generation
        risk_report = await loop.run_in_executor(
            None, self.report_agent.run,
            org_profile, asset_inventory, threat_scenarios, attack_simulations,
            fair_risk_analysis, qualitative_risk, recommended_controls, prioritized_risks
        )

        # Extract .data payloads for clean response
        def extract(result: Dict) -> Dict:
            return result.get("data", result)

        return {
            "organization_profile": extract(org_profile),
            "asset_inventory": extract(asset_inventory),
            "threat_scenarios": extract(threat_scenarios),
            "attack_simulations": extract(attack_simulations),
            "fair_risk_analysis": extract(fair_risk_analysis),
            "qualitative_risk": extract(qualitative_risk),
            "recommended_controls": extract(recommended_controls),
            "prioritized_risks": extract(prioritized_risks),
            "risk_report": extract(risk_report),
        }
