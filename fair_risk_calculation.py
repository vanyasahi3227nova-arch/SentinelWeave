"""
Agent 5: FAIR Risk Calculation Agent
Calculates FAIR risk components: LEF, LM, and Risk = LEF × LM
"""

from typing import Dict, Any, List
from rag.hybrid_rag import rag


THREAT_SCENARIO_BASELINES = {
    "ransomware": {"tef": 4, "vulnerability": 0.60, "primary_loss_pct": 0.15, "secondary_loss_pct": 0.08},
    "data breach": {"tef": 6, "vulnerability": 0.55, "primary_loss_pct": 0.10, "secondary_loss_pct": 0.06},
    "insider threat": {"tef": 2, "vulnerability": 0.45, "primary_loss_pct": 0.05, "secondary_loss_pct": 0.04},
    "phishing": {"tef": 24, "vulnerability": 0.35, "primary_loss_pct": 0.03, "secondary_loss_pct": 0.02},
    "supply chain": {"tef": 1, "vulnerability": 0.50, "primary_loss_pct": 0.20, "secondary_loss_pct": 0.10},
    "cloud misconfiguration": {"tef": 8, "vulnerability": 0.65, "primary_loss_pct": 0.08, "secondary_loss_pct": 0.05},
    "credential compromise": {"tef": 12, "vulnerability": 0.55, "primary_loss_pct": 0.07, "secondary_loss_pct": 0.04},
    "default": {"tef": 4, "vulnerability": 0.50, "primary_loss_pct": 0.08, "secondary_loss_pct": 0.05},
}

ASSET_VALUE_MAP = {
    "critical": 5_000_000,
    "high": 1_000_000,
    "medium": 250_000,
    "low": 50_000,
}


def get_threat_baseline(threat_name: str) -> Dict:
    threat_lower = threat_name.lower()
    for key, baseline in THREAT_SCENARIO_BASELINES.items():
        if key in threat_lower:
            return baseline
    return THREAT_SCENARIO_BASELINES["default"]


def compute_asset_value(assets: List[Dict]) -> float:
    total = sum(ASSET_VALUE_MAP.get(a.get("criticality", "medium"), 250_000) for a in assets)
    return total


def apply_multipliers(base_value: float, profile: Dict, fair_data: Dict) -> float:
    industry = profile.get("industry_sector", "general")
    size_cat = profile.get("organization_size", {}).get("category", "small")
    workforce = profile.get("workforce_distribution", "hybrid")
    cloud_type = profile.get("cloud_deployment_type", "single_cloud")

    ind_mult = fair_data.get("industry_risk_multiplier", {}).get(industry, 1.0)
    size_mult = fair_data.get("org_size_multiplier", {}).get(size_cat, 0.8)
    remote_mult = fair_data.get("remote_work_multiplier", {}).get(workforce, 1.0)
    cloud_mult = fair_data.get("cloud_exposure_multiplier", {}).get(cloud_type, 1.0)

    return base_value * ind_mult * size_mult * remote_mult * cloud_mult


class FAIRRiskCalculationAgent:
    """
    Implements FAIR methodology: Risk = LEF × LM
    where LEF = TEF × Vulnerability, LM = Primary Loss + Secondary Loss
    """

    def run(self, organization_profile: Dict[str, Any], asset_inventory: Dict[str, Any], threat_scenarios: Dict[str, Any]) -> Dict[str, Any]:
        profile = organization_profile.get("data", organization_profile)
        assets_data = asset_inventory.get("data", asset_inventory)
        threats_data = threat_scenarios.get("data", threat_scenarios)

        fair_data = rag.get_fair_baseline()
        assets = assets_data.get("assets", [])
        threat_list = threats_data.get("threat_scenarios", [])

        total_asset_value = compute_asset_value(assets)
        adjusted_asset_value = apply_multipliers(total_asset_value, profile, fair_data)

        risk_calculations = []
        aggregate_annual_loss = 0.0

        for threat in threat_list:
            threat_name = threat.get("threat_name", "Unknown")
            baseline = get_threat_baseline(threat_name)

            # Threat Event Frequency (per year)
            tef = baseline["tef"]

            # Vulnerability probability (probability that a threat event results in loss)
            vuln = baseline["vulnerability"]

            # Loss Event Frequency (LEF) = TEF × Vulnerability
            lef = tef * vuln

            # Primary Loss Magnitude
            primary_loss = adjusted_asset_value * baseline["primary_loss_pct"]

            # Secondary Loss Magnitude
            secondary_loss = adjusted_asset_value * baseline["secondary_loss_pct"]

            # Total Loss Magnitude
            lm = primary_loss + secondary_loss

            # Annual Risk Exposure = LEF × LM
            annual_risk = lef * lm

            aggregate_annual_loss += annual_risk

            # Risk rating
            if annual_risk > 2_000_000:
                risk_rating = "critical"
            elif annual_risk > 500_000:
                risk_rating = "high"
            elif annual_risk > 100_000:
                risk_rating = "medium"
            else:
                risk_rating = "low"

            risk_calculations.append({
                "threat_id": threat.get("id", f"TS-{len(risk_calculations)+1:03d}"),
                "threat_name": threat_name,
                "fair_components": {
                    "threat_event_frequency_tef": round(tef, 2),
                    "vulnerability_probability": round(vuln, 3),
                    "loss_event_frequency_lef": round(lef, 4),
                    "primary_loss_magnitude_usd": round(primary_loss, 2),
                    "secondary_loss_magnitude_usd": round(secondary_loss, 2),
                    "total_loss_magnitude_lm_usd": round(lm, 2),
                },
                "annual_risk_exposure_usd": round(annual_risk, 2),
                "risk_rating": risk_rating,
            })

        # Sort by annual risk exposure descending
        risk_calculations.sort(key=lambda x: x["annual_risk_exposure_usd"], reverse=True)

        return {
            "status": "success",
            "agent": "fair_risk_calculation",
            "data": {
                "risk_calculations": risk_calculations,
                "summary": {
                    "total_asset_value_usd": round(total_asset_value, 2),
                    "adjusted_asset_value_usd": round(adjusted_asset_value, 2),
                    "aggregate_annual_loss_exposure_usd": round(aggregate_annual_loss, 2),
                    "risk_rating_distribution": {
                        "critical": sum(1 for r in risk_calculations if r["risk_rating"] == "critical"),
                        "high": sum(1 for r in risk_calculations if r["risk_rating"] == "high"),
                        "medium": sum(1 for r in risk_calculations if r["risk_rating"] == "medium"),
                        "low": sum(1 for r in risk_calculations if r["risk_rating"] == "low"),
                    }
                },
                "methodology": "FAIR (Factor Analysis of Information Risk)",
            }
        }
