"""
Agent 6: Qualitative Risk Analysis Agent
Provides qualitative analysis: risk severity, narratives, business impact.
"""

from typing import Dict, Any, List


RISK_NARRATIVES = {
    "critical": (
        "This risk presents an existential threat to the organization. Immediate executive attention "
        "and emergency remediation resources are required. A successful attack in this scenario could "
        "result in complete business disruption, severe regulatory penalties, and irreparable reputational damage."
    ),
    "high": (
        "This risk represents a significant threat that could substantially impact business operations. "
        "Senior management involvement is required and remediation should be treated as a high-priority "
        "initiative. Left unaddressed, this risk could result in major financial losses and regulatory action."
    ),
    "medium": (
        "This risk poses a moderate threat to business continuity and data security. While not immediately "
        "critical, a structured remediation plan should be developed and executed within the next quarter. "
        "Continued monitoring is essential to detect any escalation."
    ),
    "low": (
        "This risk presents a limited threat in the current environment. Standard security controls and "
        "periodic monitoring should be maintained. This risk should be reviewed annually or when the "
        "threat landscape changes significantly."
    ),
}

REGULATORY_IMPACT = {
    "HIPAA": "HIPAA breach notification required within 60 days. OCR fines range $100–$50,000 per violation.",
    "PCI-DSS": "Mandatory breach notification to card brands. Potential loss of card processing privileges.",
    "GDPR": "72-hour notification to supervisory authority. Fines up to 4% of global annual revenue.",
    "CCPA": "Statutory damages of $100–$750 per consumer per incident.",
    "SOC2": "Loss of SOC2 certification impacting customer trust and enterprise contracts.",
    "FERPA": "Loss of federal funding eligibility for educational institutions.",
    "SOX": "Criminal penalties for knowingly false financial certifications.",
}


class QualitativeRiskAnalysisAgent:
    """
    Generates qualitative risk assessments including severity labels,
    narratives, and business impact descriptions.
    """

    def run(self, fair_risk_analysis: Dict[str, Any], organization_profile: Dict[str, Any]) -> Dict[str, Any]:
        fair_data = fair_risk_analysis.get("data", fair_risk_analysis)
        profile = organization_profile.get("data", organization_profile)

        risk_calcs = fair_data.get("risk_calculations", [])
        regulations = profile.get("regulatory_exposure", [])

        qualitative_assessments = []

        for risk in risk_calcs:
            rating = risk.get("risk_rating", "medium")
            threat_name = risk.get("threat_name", "Unknown Threat")
            annual_exposure = risk.get("annual_risk_exposure_usd", 0)

            narrative = RISK_NARRATIVES.get(rating, RISK_NARRATIVES["medium"])

            # Regulatory impact
            reg_impacts = []
            for reg in regulations:
                if reg in REGULATORY_IMPACT:
                    reg_impacts.append({"regulation": reg, "impact": REGULATORY_IMPACT[reg]})

            qualitative_assessments.append({
                "threat_id": risk.get("threat_id"),
                "threat_name": threat_name,
                "risk_rating": rating,
                "risk_label": rating.upper(),
                "annual_loss_exposure_usd": annual_exposure,
                "risk_narrative": narrative,
                "business_impact": _generate_business_impact(threat_name, rating),
                "regulatory_implications": reg_impacts[:3],
                "recommended_response": _get_response_strategy(rating),
                "monitoring_priority": "immediate" if rating == "critical" else ("high" if rating == "high" else "standard"),
            })

        # Overall risk posture
        critical_count = sum(1 for a in qualitative_assessments if a["risk_rating"] == "critical")
        high_count = sum(1 for a in qualitative_assessments if a["risk_rating"] == "high")

        if critical_count > 0:
            overall_posture = "CRITICAL - Immediate Action Required"
        elif high_count > 1:
            overall_posture = "HIGH RISK - Urgent Remediation Needed"
        elif high_count > 0:
            overall_posture = "ELEVATED RISK - Prioritized Remediation Required"
        else:
            overall_posture = "MODERATE RISK - Structured Risk Management Program Required"

        return {
            "status": "success",
            "agent": "qualitative_risk_analysis",
            "data": {
                "qualitative_assessments": qualitative_assessments,
                "overall_risk_posture": overall_posture,
                "regulatory_context": [
                    {"regulation": reg, "impact": REGULATORY_IMPACT.get(reg, "Regulatory compliance required")}
                    for reg in regulations
                ],
                "risk_summary": {
                    "critical_risks": critical_count,
                    "high_risks": high_count,
                    "medium_risks": sum(1 for a in qualitative_assessments if a["risk_rating"] == "medium"),
                    "low_risks": sum(1 for a in qualitative_assessments if a["risk_rating"] == "low"),
                }
            }
        }


def _generate_business_impact(threat_name: str, rating: str) -> Dict[str, str]:
    severity_text = {"critical": "catastrophic", "high": "significant", "medium": "moderate", "low": "minor"}
    impact_level = severity_text.get(rating, "moderate")
    return {
        "operational_impact": f"Potential {impact_level} disruption to business operations and service delivery.",
        "financial_impact": f"{impact_level.capitalize()} financial losses including remediation, legal, and regulatory costs.",
        "reputational_impact": f"Customer trust and brand reputation may suffer {impact_level} damage.",
        "strategic_impact": f"Business continuity and competitive position may be {impact_level}ly affected.",
    }


def _get_response_strategy(rating: str) -> str:
    strategies = {
        "critical": "TREAT - Immediate mitigation required. Allocate emergency resources. Executive escalation mandatory.",
        "high": "TREAT - Develop and execute remediation plan within 30 days. Assign dedicated owner.",
        "medium": "TREAT/TOLERATE - Remediation plan required within 90 days. Accept residual risk with documented justification.",
        "low": "TOLERATE/MONITOR - Accept with compensating controls. Annual review required.",
    }
    return strategies.get(rating, strategies["medium"])
