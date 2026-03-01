"""
Agent 3: Threat Intelligence Agent
Identifies relevant threats using hybrid RAG retrieval.
"""

from typing import Dict, Any, List
from rag.hybrid_rag import rag
import json


ASSET_THREAT_MAP = {
    "database": ["sql_injection", "data_breach", "ransomware", "insider_threat", "credential_compromise"],
    "web_application": ["web_application_attack", "sql_injection", "xss", "api_abuse", "credential_stuffing"],
    "cloud": ["cloud_misconfiguration", "data_exposure", "credential_compromise", "supply_chain_attack"],
    "identity": ["credential_compromise", "account_takeover", "phishing", "brute_force"],
    "endpoint": ["malware", "ransomware", "phishing", "insider_threat"],
    "email": ["phishing", "business_email_compromise", "malware"],
    "vpn": ["credential_compromise", "brute_force", "vulnerability_exploitation"],
    "payment": ["skimming", "fraud", "pci_breach"],
    "backup": ["ransomware", "data_destruction"],
    "api": ["api_abuse", "authentication_bypass", "data_exfiltration"],
}


def map_asset_to_threat_categories(asset: Dict) -> List[str]:
    name_lower = asset["name"].lower()
    categories = []
    for key, threats in ASSET_THREAT_MAP.items():
        if key in name_lower:
            categories.extend(threats)
    return list(set(categories)) or ["general_threat"]


class ThreatIntelligenceAgent:
    """
    Uses hybrid RAG to identify relevant MITRE ATT&CK techniques
    and industry-specific threat scenarios.
    """

    def run(self, organization_profile: Dict[str, Any], asset_inventory: Dict[str, Any]) -> Dict[str, Any]:
        profile = organization_profile.get("data", organization_profile)
        assets_data = asset_inventory.get("data", asset_inventory)

        industry = profile.get("industry_sector", "general")
        assets = assets_data.get("assets", [])

        # Vector search for industry threats
        industry_query = f"{industry} cybersecurity threats attack"
        industry_threat_docs = rag.search_industry_threats(industry_query, top_k=3)

        # Get primary industry threat info
        primary_threat_doc = industry_threat_docs[0] if industry_threat_docs else {}
        top_threats = primary_threat_doc.get("top_threats", [
            "Phishing", "Ransomware", "Credential Compromise", "Data Breach"
        ])
        threat_actors = primary_threat_doc.get("threat_actors", ["Financially Motivated Cybercriminals"])
        avg_breach_cost = primary_threat_doc.get("avg_breach_cost", 4350000)

        # Vector search for MITRE techniques per threat
        mitre_techniques = []
        seen_technique_ids = set()
        for threat in top_threats[:5]:
            techniques = rag.search_mitre_techniques(threat, top_k=3)
            for t in techniques:
                if t.get("id") not in seen_technique_ids:
                    seen_technique_ids.add(t.get("id"))
                    mitre_techniques.append({
                        "id": t.get("id"),
                        "name": t.get("name"),
                        "tactic": t.get("tactic"),
                        "severity": t.get("severity", "medium"),
                        "likelihood": t.get("likelihood", 0.5),
                        "description": t.get("description", ""),
                        "related_threat": threat,
                    })

        # Structured asset-threat mapping
        asset_threat_matrix = []
        for asset in assets[:15]:
            threat_cats = map_asset_to_threat_categories(asset)
            asset_threat_matrix.append({
                "asset": asset["name"],
                "asset_criticality": asset["criticality"],
                "threat_categories": threat_cats[:4],
            })

        # Compile threat scenarios
        threat_scenarios = []
        for i, threat in enumerate(top_threats):
            severity = "critical" if i < 2 else ("high" if i < 4 else "medium")
            relevant_techniques = [t for t in mitre_techniques if t.get("related_threat") == threat][:3]
            threat_scenarios.append({
                "id": f"TS-{i+1:03d}",
                "threat_name": threat,
                "severity": severity,
                "threat_actors": threat_actors,
                "mitre_techniques": relevant_techniques,
                "affected_assets": [
                    a["asset"] for a in asset_threat_matrix
                    if any(tc in str(threat).lower().replace(" ", "_") for tc in a["threat_categories"])
                ][:5],
            })

        return {
            "status": "success",
            "agent": "threat_intelligence",
            "data": {
                "threat_scenarios": threat_scenarios,
                "mitre_techniques_identified": mitre_techniques,
                "asset_threat_matrix": asset_threat_matrix,
                "threat_actor_profiles": [
                    {"name": actor, "motivation": "financial" if "financial" in actor.lower() else "strategic"}
                    for actor in threat_actors
                ],
                "industry_breach_stats": {
                    "avg_breach_cost_usd": avg_breach_cost,
                    "sector": industry,
                },
            }
        }
