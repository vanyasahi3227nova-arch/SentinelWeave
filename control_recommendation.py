"""
Agent 7: Control Recommendation Agent
Recommends security controls mapped to NIST CSF and CIS Controls.
"""

from typing import Dict, Any, List
from rag.hybrid_rag import rag


THREAT_CATEGORY_MAPPING = {
    "ransomware": ["ransomware", "malware", "data_destruction", "business_disruption"],
    "data breach": ["data_breach", "data_exfiltration", "cloud_breach"],
    "phishing": ["phishing", "social_engineering", "business_email_compromise"],
    "insider threat": ["insider_threat", "data_exfiltration"],
    "credential": ["credential_compromise", "account_takeover", "brute_force"],
    "supply chain": ["supply_chain_attack", "third_party_breach"],
    "cloud": ["cloud_misconfiguration", "data_exposure"],
}

INDUSTRY_SPECIFIC_CONTROLS = {
    "healthcare": [
        {"id": "HC-001", "name": "PHI Encryption at Rest and in Transit", "description": "Encrypt all PHI using AES-256 at rest and TLS 1.2+ in transit as required by HIPAA.", "nist_csf": "PR.DS-1", "priority": "critical"},
        {"id": "HC-002", "name": "Audit Logging of PHI Access", "description": "Comprehensive audit trails for all PHI access as required by HIPAA Security Rule.", "nist_csf": "PR.PT-1", "priority": "critical"},
        {"id": "HC-003", "name": "BAA Management Program", "description": "Business Associate Agreements with all vendors handling PHI.", "nist_csf": "ID.SC-2", "priority": "high"},
    ],
    "finance": [
        {"id": "FIN-001", "name": "PCI-DSS Compliance Program", "description": "Full PCI-DSS compliance for cardholder data environment.", "nist_csf": "PR.DS-1", "priority": "critical"},
        {"id": "FIN-002", "name": "Anti-Fraud Monitoring", "description": "Real-time transaction monitoring and fraud detection systems.", "nist_csf": "DE.CM-1", "priority": "critical"},
        {"id": "FIN-003", "name": "SOX IT Controls", "description": "IT general controls supporting SOX financial reporting.", "nist_csf": "PR.IP-1", "priority": "high"},
    ],
    "technology": [
        {"id": "TECH-001", "name": "Secure SDLC", "description": "Integrate security into software development lifecycle with SAST/DAST tools.", "nist_csf": "PR.IP-2", "priority": "high"},
        {"id": "TECH-002", "name": "API Security Gateway", "description": "Implement API gateway with authentication, rate limiting, and threat protection.", "nist_csf": "PR.AC-3", "priority": "high"},
        {"id": "TECH-003", "name": "Container Security", "description": "Image scanning, runtime protection, and secure Kubernetes configuration.", "nist_csf": "PR.DS-7", "priority": "medium"},
    ],
}


class ControlRecommendationAgent:
    """
    Recommends security controls based on identified risks using
    NIST CSF and CIS Controls frameworks.
    """

    def run(self, threat_scenarios: Dict[str, Any], fair_risk_analysis: Dict[str, Any], organization_profile: Dict[str, Any]) -> Dict[str, Any]:
        threats_data = threat_scenarios.get("data", threat_scenarios)
        fair_data = fair_risk_analysis.get("data", fair_risk_analysis)
        profile = organization_profile.get("data", organization_profile)

        industry = profile.get("industry_sector", "general")
        threat_list = threats_data.get("threat_scenarios", [])
        high_risk = [r for r in fair_data.get("risk_calculations", []) if r.get("risk_rating") in ["critical", "high"]]

        # Build threat categories from top risks
        threat_categories = []
        for threat in threat_list[:6]:
            threat_name = threat.get("threat_name", "").lower()
            for key, cats in THREAT_CATEGORY_MAPPING.items():
                if key in threat_name:
                    threat_categories.extend(cats)

        threat_categories = list(set(threat_categories))

        # Get base controls from structured lookup
        base_controls = rag.get_controls(threat_categories)

        # Add industry-specific controls
        industry_controls = INDUSTRY_SPECIFIC_CONTROLS.get(industry, [])

        # Structure recommendations
        immediate_controls = []
        short_term_controls = []
        long_term_controls = []

        for ctrl in base_controls:
            control_rec = {
                "control_id": ctrl.get("id"),
                "name": ctrl.get("name"),
                "description": ctrl.get("description"),
                "nist_csf_reference": ctrl.get("nist_csf"),
                "cis_control_reference": ctrl.get("cis_control"),
                "implementation_effort": ctrl.get("effort", "medium"),
                "expected_impact": ctrl.get("impact", "high"),
                "threat_categories_addressed": ctrl.get("threat_categories", []),
            }
            effort = ctrl.get("effort", "medium")
            priority = ctrl.get("priority", 5)

            if effort == "low" and int(priority) <= 5:
                immediate_controls.append(control_rec)
            elif effort in ["medium"] or int(priority) <= 10:
                short_term_controls.append(control_rec)
            else:
                long_term_controls.append(control_rec)

        for ctrl in industry_controls:
            control_rec = {
                "control_id": ctrl.get("id"),
                "name": ctrl.get("name"),
                "description": ctrl.get("description"),
                "nist_csf_reference": ctrl.get("nist_csf"),
                "cis_control_reference": "Industry-Specific",
                "implementation_effort": "medium",
                "expected_impact": ctrl.get("priority", "high"),
                "threat_categories_addressed": ["industry_compliance"],
                "industry_specific": True,
            }
            if ctrl.get("priority") == "critical":
                immediate_controls.insert(0, control_rec)
            else:
                short_term_controls.insert(0, control_rec)

        return {
            "status": "success",
            "agent": "control_recommendation",
            "data": {
                "immediate_controls": immediate_controls[:5],
                "short_term_controls": short_term_controls[:6],
                "long_term_controls": long_term_controls[:4],
                "total_controls_recommended": len(immediate_controls) + len(short_term_controls) + len(long_term_controls),
                "frameworks_applied": ["NIST CSF", "CIS Controls v8", "Industry-Specific Standards"],
                "industry": industry,
            }
        }
