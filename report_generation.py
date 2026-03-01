"""
Agent 9: Report Generation Agent
Aggregates all outputs into a final comprehensive risk report.
"""

from typing import Dict, Any
import time


class ReportGenerationAgent:
    """
    Produces a structured executive risk report combining all agent outputs.
    """

    def run(self, organization_profile: Dict, asset_inventory: Dict,
            threat_scenarios: Dict, attack_simulations: Dict,
            fair_risk_analysis: Dict, qualitative_risk: Dict,
            recommended_controls: Dict, prioritized_risks: Dict) -> Dict[str, Any]:

        profile = organization_profile.get("data", organization_profile)
        assets_data = asset_inventory.get("data", asset_inventory)
        fair_data = fair_risk_analysis.get("data", fair_risk_analysis)
        qualitative_data = qualitative_risk.get("data", qualitative_risk)
        controls_data = recommended_controls.get("data", recommended_controls)
        priority_data = prioritized_risks.get("data", prioritized_risks)
        sims_data = attack_simulations.get("data", attack_simulations)

        industry = profile.get("industry_sector", "Unknown").title()
        org_size = profile.get("organization_size", {})
        regulations = profile.get("regulatory_exposure", [])

        total_assets = assets_data.get("summary", {}).get("total_assets", 0)
        aggregate_loss = fair_data.get("summary", {}).get("aggregate_annual_loss_exposure_usd", 0)
        overall_posture = qualitative_data.get("overall_risk_posture", "Unknown")
        risk_summary = qualitative_data.get("risk_summary", {})

        top_actions = priority_data.get("top_priority_actions", [])
        immediate_controls = controls_data.get("immediate_controls", [])[:3]
        prioritized_register = priority_data.get("prioritized_risk_register", [])[:5]
        top_simulations = sims_data.get("attack_simulations", [])[:3]

        report = {
            "report_metadata": {
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "report_type": "Cyber Risk Analysis and Threat Model Report",
                "methodology": "FAIR (Factor Analysis of Information Risk) + MITRE ATT&CK",
                "frameworks": ["FAIR", "MITRE ATT&CK", "NIST CSF", "CIS Controls v8"],
                "version": "1.0",
            },
            "executive_summary": {
                "organization_profile": {
                    "industry": industry,
                    "employees": org_size.get("employee_count", "Unknown"),
                    "size_category": org_size.get("category", "Unknown"),
                    "regulatory_exposure": regulations,
                    "cloud_providers": profile.get("cloud_providers", []),
                    "workforce_distribution": profile.get("workforce_distribution", "Unknown"),
                },
                "overall_risk_posture": overall_posture,
                "aggregate_annual_loss_exposure_usd": round(aggregate_loss, 2),
                "total_assets_identified": total_assets,
                "risk_distribution": risk_summary,
                "key_findings": _generate_key_findings(profile, fair_data, qualitative_data),
            },
            "top_risks": prioritized_register,
            "immediate_action_items": top_actions,
            "priority_controls": [
                {
                    "control_id": ctrl.get("control_id"),
                    "name": ctrl.get("name"),
                    "description": ctrl.get("description"),
                    "effort": ctrl.get("implementation_effort"),
                }
                for ctrl in immediate_controls
            ],
            "attack_scenarios_summary": [
                {
                    "simulation_id": sim.get("simulation_id"),
                    "threat": sim.get("threat_name"),
                    "stages": sim.get("total_stages"),
                    "success_probability": sim.get("attack_feasibility", {}).get("success_probability"),
                    "duration": sim.get("attack_duration_estimate"),
                }
                for sim in top_simulations
            ],
            "compliance_considerations": [
                {"regulation": reg, "status": "Review Required", "priority": "high"}
                for reg in regulations
            ],
            "risk_roadmap": {
                "immediate_0_30_days": [
                    f"Implement {ctrl.get('name')}" for ctrl in immediate_controls[:3]
                ],
                "short_term_30_90_days": [
                    f"Deploy {ctrl.get('name')}"
                    for ctrl in controls_data.get("short_term_controls", [])[:3]
                ],
                "long_term_90_365_days": [
                    f"Establish {ctrl.get('name')}"
                    for ctrl in controls_data.get("long_term_controls", [])[:3]
                ],
            },
        }

        return {
            "status": "success",
            "agent": "report_generation",
            "data": report
        }


def _generate_key_findings(profile: Dict, fair_data: Dict, qualitative_data: Dict) -> list:
    findings = []
    industry = profile.get("industry_sector", "general")
    regulations = profile.get("regulatory_exposure", [])
    aggregate_loss = fair_data.get("summary", {}).get("aggregate_annual_loss_exposure_usd", 0)
    risk_summary = qualitative_data.get("risk_summary", {})

    findings.append(
        f"Aggregate annual cyber risk exposure estimated at ${aggregate_loss:,.0f} based on FAIR analysis."
    )

    if risk_summary.get("critical", 0) > 0:
        findings.append(
            f"{risk_summary['critical']} critical risk(s) identified requiring immediate executive action."
        )

    if regulations:
        findings.append(
            f"Organization is subject to {', '.join(regulations[:3])} regulatory requirements, "
            "increasing breach notification and penalty exposure."
        )

    workforce = profile.get("workforce_distribution", "")
    if "remote" in workforce:
        findings.append(
            "Remote/hybrid workforce significantly expands the attack surface through endpoint and VPN exposure."
        )

    cloud_providers = profile.get("cloud_providers", [])
    if cloud_providers and "Unknown" not in str(cloud_providers):
        findings.append(
            f"Cloud infrastructure ({', '.join(cloud_providers[:2])}) introduces cloud-specific risks "
            "including misconfiguration and unauthorized access."
        )

    return findings[:5]
