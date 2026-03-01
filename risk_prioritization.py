"""
Agent 8: Risk Prioritization Agent
Ranks and prioritizes risks by composite score.
"""

from typing import Dict, Any, List


SEVERITY_SCORE = {"critical": 4, "high": 3, "medium": 2, "low": 1}
LIKELIHOOD_SCORE = {"very_high": 5, "high": 4, "medium": 3, "low": 2, "very_low": 1}


def compute_priority_score(risk: Dict, qualitative: Dict) -> float:
    """
    Composite priority score combining:
    - Annual risk exposure (financial)
    - Risk rating (severity)
    - Asset criticality
    """
    annual_loss = risk.get("annual_risk_exposure_usd", 0)
    rating = risk.get("risk_rating", "medium")
    severity_weight = SEVERITY_SCORE.get(rating, 2)

    # Normalize financial loss to 0-5 scale
    if annual_loss > 5_000_000:
        financial_score = 5.0
    elif annual_loss > 1_000_000:
        financial_score = 4.0
    elif annual_loss > 500_000:
        financial_score = 3.0
    elif annual_loss > 100_000:
        financial_score = 2.0
    else:
        financial_score = 1.0

    return (severity_weight * 0.4) + (financial_score * 0.6)


class RiskPrioritizationAgent:
    """
    Produces a prioritized risk register with composite scoring.
    """

    def run(self, fair_risk_analysis: Dict[str, Any], qualitative_risk: Dict[str, Any],
            recommended_controls: Dict[str, Any]) -> Dict[str, Any]:

        fair_data = fair_risk_analysis.get("data", fair_risk_analysis)
        qualitative_data = qualitative_risk.get("data", qualitative_risk)
        controls_data = recommended_controls.get("data", recommended_controls)

        risk_calcs = fair_data.get("risk_calculations", [])
        qualitative_list = qualitative_data.get("qualitative_assessments", [])

        # Create lookup by threat_id
        qual_lookup = {q.get("threat_id"): q for q in qualitative_list}

        prioritized = []
        for i, risk in enumerate(risk_calcs):
            threat_id = risk.get("threat_id")
            qual = qual_lookup.get(threat_id, {})

            priority_score = compute_priority_score(risk, qual)

            prioritized.append({
                "priority_rank": i + 1,  # Will be set after sorting
                "threat_id": threat_id,
                "threat_name": risk.get("threat_name"),
                "risk_rating": risk.get("risk_rating"),
                "annual_loss_exposure_usd": risk.get("annual_risk_exposure_usd"),
                "priority_score": round(priority_score, 3),
                "recommended_response": qual.get("recommended_response", "N/A"),
                "monitoring_priority": qual.get("monitoring_priority", "standard"),
                "fair_lef": risk.get("fair_components", {}).get("loss_event_frequency_lef"),
                "fair_lm": risk.get("fair_components", {}).get("total_loss_magnitude_lm_usd"),
            })

        # Sort by priority score descending
        prioritized.sort(key=lambda x: x["priority_score"], reverse=True)

        # Assign ranks
        for i, item in enumerate(prioritized):
            item["priority_rank"] = i + 1

        # Build top 3 action items
        top_actions = []
        for risk in prioritized[:3]:
            top_actions.append({
                "rank": risk["priority_rank"],
                "threat": risk["threat_name"],
                "action": f"Immediate risk treatment required for {risk['threat_name']}. "
                          f"Annual exposure: ${risk['annual_loss_exposure_usd']:,.0f}",
            })

        return {
            "status": "success",
            "agent": "risk_prioritization",
            "data": {
                "prioritized_risk_register": prioritized,
                "top_priority_actions": top_actions,
                "risk_treatment_summary": {
                    "treat_immediately": [r for r in prioritized if r["risk_rating"] in ["critical"]],
                    "treat_short_term": [r for r in prioritized if r["risk_rating"] == "high"],
                    "monitor_and_review": [r for r in prioritized if r["risk_rating"] in ["medium", "low"]],
                }
            }
        }
