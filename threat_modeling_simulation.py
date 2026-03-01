"""
Agent 4: Threat Modeling Simulation Agent
Simulates realistic attack scenarios using kill chain logic.
"""

from typing import Dict, Any, List
import json


KILL_CHAIN_TEMPLATES = {
    "ransomware": [
        {"phase": "Initial Access", "technique": "T1566 - Phishing", "description": "Attacker sends spear-phishing email with malicious attachment to employee."},
        {"phase": "Execution", "technique": "T1059 - Command and Scripting Interpreter", "description": "Malicious macro or script executes on victim endpoint."},
        {"phase": "Persistence", "technique": "T1547 - Boot or Logon Autostart Execution", "description": "Malware establishes persistence mechanism."},
        {"phase": "Privilege Escalation", "technique": "T1548 - Abuse Elevation Control Mechanism", "description": "Attacker escalates to administrator privileges."},
        {"phase": "Defense Evasion", "technique": "T1562 - Impair Defenses", "description": "Attacker disables or impairs endpoint security tools."},
        {"phase": "Lateral Movement", "technique": "T1021 - Remote Services", "description": "Attacker moves laterally to additional systems using stolen credentials."},
        {"phase": "Collection", "technique": "T1005 - Data from Local System", "description": "Attacker identifies and stages valuable data."},
        {"phase": "Impact", "technique": "T1486 - Data Encrypted for Impact", "description": "Ransomware encrypts files and demands ransom payment."},
    ],
    "data_breach": [
        {"phase": "Initial Access", "technique": "T1190 - Exploit Public-Facing Application", "description": "Attacker exploits vulnerability in internet-facing web application."},
        {"phase": "Execution", "technique": "T1059 - Command and Scripting Interpreter", "description": "Attacker executes commands on compromised web server."},
        {"phase": "Credential Access", "technique": "T1552 - Unsecured Credentials", "description": "Attacker discovers hardcoded credentials or secrets."},
        {"phase": "Discovery", "technique": "T1580 - Cloud Infrastructure Discovery", "description": "Attacker enumerates cloud resources and data stores."},
        {"phase": "Collection", "technique": "T1530 - Data from Cloud Storage Object", "description": "Attacker accesses sensitive data in cloud storage buckets."},
        {"phase": "Exfiltration", "technique": "T1567 - Exfiltration Over Web Service", "description": "Attacker exfiltrates data to attacker-controlled cloud storage."},
    ],
    "insider_threat": [
        {"phase": "Initial Access", "technique": "T1078 - Valid Accounts", "description": "Insider uses their legitimate credentials to access systems."},
        {"phase": "Discovery", "technique": "T1083 - File and Directory Discovery", "description": "Insider browses file systems searching for valuable data."},
        {"phase": "Collection", "technique": "T1005 - Data from Local System", "description": "Insider copies sensitive files and records."},
        {"phase": "Exfiltration", "technique": "T1052 - Exfiltration Over Physical Medium", "description": "Insider exfiltrates data via USB or personal cloud storage."},
    ],
    "credential_compromise": [
        {"phase": "Initial Access", "technique": "T1078 - Valid Accounts", "description": "Attacker uses stolen credentials from phishing or credential stuffing."},
        {"phase": "Persistence", "technique": "T1078 - Valid Accounts", "description": "Attacker maintains access using legitimate credentials."},
        {"phase": "Privilege Escalation", "technique": "T1548 - Abuse Elevation Control Mechanism", "description": "Attacker escalates privileges from standard user."},
        {"phase": "Lateral Movement", "technique": "T1021 - Remote Services", "description": "Attacker pivots to other systems using discovered credentials."},
        {"phase": "Collection", "technique": "T1530 - Data from Cloud Storage Object", "description": "Attacker accesses cloud data and email content."},
        {"phase": "Exfiltration", "technique": "T1537 - Transfer Data to Cloud Account", "description": "Attacker transfers data to external cloud account."},
    ],
    "supply_chain_attack": [
        {"phase": "Initial Access", "technique": "T1195 - Supply Chain Compromise", "description": "Attacker compromises a trusted third-party software vendor or service."},
        {"phase": "Execution", "technique": "T1059 - Command and Scripting Interpreter", "description": "Malicious code from compromised dependency executes."},
        {"phase": "Persistence", "technique": "T1546 - Event Triggered Execution", "description": "Backdoor triggers on specific conditions in target environment."},
        {"phase": "Collection", "technique": "T1005 - Data from Local System", "description": "Attacker collects sensitive configuration and customer data."},
        {"phase": "Exfiltration", "technique": "T1041 - Exfiltration Over C2 Channel", "description": "Data exfiltrated through established C2 channel."},
    ],
}

THREAT_TO_SIMULATION_MAP = {
    "ransomware": "ransomware",
    "data breach": "data_breach",
    "insider threat": "insider_threat",
    "credential": "credential_compromise",
    "phishing": "credential_compromise",
    "supply chain": "supply_chain_attack",
    "third-party": "supply_chain_attack",
}


def get_simulation_template(threat_name: str) -> str:
    threat_lower = threat_name.lower()
    for keyword, template_key in THREAT_TO_SIMULATION_MAP.items():
        if keyword in threat_lower:
            return template_key
    return "data_breach"


def estimate_attack_duration(template_key: str) -> str:
    durations = {
        "ransomware": "2-14 days from initial access to encryption",
        "data_breach": "Days to months (average dwell time: 207 days)",
        "insider_threat": "Weeks to months",
        "credential_compromise": "Hours to days",
        "supply_chain_attack": "Weeks to months",
    }
    return durations.get(template_key, "Days to weeks")


class ThreatModelingSimulationAgent:
    """
    Simulates attack chains using kill chain logic and MITRE ATT&CK mappings.
    """

    def run(self, threat_scenarios: Dict[str, Any], asset_inventory: Dict[str, Any]) -> Dict[str, Any]:
        scenarios_data = threat_scenarios.get("data", threat_scenarios)
        assets_data = asset_inventory.get("data", asset_inventory)

        threat_list = scenarios_data.get("threat_scenarios", [])
        assets = assets_data.get("assets", [])
        critical_assets = [a["name"] for a in assets if a.get("criticality") in ["critical", "high"]][:5]

        simulations = []
        for i, threat in enumerate(threat_list[:6]):
            threat_name = threat.get("threat_name", "Unknown Threat")
            template_key = get_simulation_template(threat_name)
            kill_chain = KILL_CHAIN_TEMPLATES.get(template_key, KILL_CHAIN_TEMPLATES["data_breach"])

            severity = threat.get("severity", "medium")
            success_prob = {"critical": 0.65, "high": 0.50, "medium": 0.35, "low": 0.20}.get(severity, 0.40)

            simulations.append({
                "simulation_id": f"SIM-{i+1:03d}",
                "threat_name": threat_name,
                "scenario_id": threat.get("id", f"TS-{i+1:03d}"),
                "attack_template": template_key,
                "kill_chain_stages": kill_chain,
                "total_stages": len(kill_chain),
                "targeted_assets": critical_assets[:3],
                "attack_feasibility": {
                    "success_probability": success_prob,
                    "complexity": "medium" if success_prob > 0.5 else "high",
                    "attacker_skill_required": "intermediate" if success_prob > 0.5 else "advanced",
                },
                "attack_duration_estimate": estimate_attack_duration(template_key),
                "business_impact": _estimate_business_impact(threat_name, severity),
            })

        return {
            "status": "success",
            "agent": "threat_modeling_simulation",
            "data": {
                "attack_simulations": simulations,
                "total_simulations": len(simulations),
                "high_risk_simulations": sum(1 for s in simulations if s["attack_feasibility"]["success_probability"] >= 0.5),
            }
        }


def _estimate_business_impact(threat_name: str, severity: str) -> Dict[str, str]:
    impacts = {
        "ransomware": {
            "operational": "Complete system outage for 1-4 weeks",
            "financial": "Ransom demand + recovery costs + lost business",
            "reputational": "High - public disclosure likely",
            "regulatory": "Mandatory breach notification required",
        },
        "data breach": {
            "operational": "Moderate disruption during investigation",
            "financial": "Legal fees + regulatory fines + notification costs",
            "reputational": "High - customer trust erosion",
            "regulatory": "Mandatory reporting to regulators",
        },
        "insider threat": {
            "operational": "Limited disruption",
            "financial": "IP theft value + investigation costs",
            "reputational": "Medium - if not publicly disclosed",
            "regulatory": "Depends on data accessed",
        },
    }
    threat_lower = threat_name.lower()
    for key, impact in impacts.items():
        if key in threat_lower:
            return impact
    return {
        "operational": f"Variable disruption based on {severity} severity",
        "financial": "Investigation, remediation, and potential regulatory costs",
        "reputational": "Depends on breach scope and disclosure",
        "regulatory": "May require regulatory notification",
    }
