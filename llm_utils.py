"""
LLM Utility Module
Provides structured reasoning over natural language descriptions.
Uses rule-based extraction with optional HuggingFace LLM augmentation.
"""

import re
from typing import Dict, Any, List, Optional


# ─── Keyword dictionaries ───
INDUSTRY_KEYWORDS = {
    "healthcare": ["health", "medical", "patient", "hospital", "clinic", "pharma", "hipaa", "ehr", "emr", "telemedicine", "doctor", "nurse", "healthcare"],
    "finance": ["bank", "financ", "insurance", "invest", "trading", "payment", "fintech", "credit", "loan", "mortgage", "wealth"],
    "retail": ["retail", "ecommerce", "e-commerce", "shop", "store", "merchandise", "inventory", "pos", "point of sale"],
    "technology": ["saas", "software", "tech", "cloud", "developer", "startup", "platform", "api", "data", "ai", "ml"],
    "education": ["school", "university", "college", "education", "student", "learning", "academic", "course", "lms"],
    "manufacturing": ["manufactur", "factory", "industrial", "production", "supply chain", "warehouse", "scada", "ics"],
    "legal": ["law firm", "legal", "attorney", "lawyer", "court", "compliance", "contract"],
}

CLOUD_PROVIDERS = {
    "AWS": ["aws", "amazon web services", "s3", "ec2", "lambda", "rds"],
    "Azure": ["azure", "microsoft azure", "office 365", "o365", "sharepoint"],
    "GCP": ["gcp", "google cloud", "google cloud platform", "bigquery", "gke"],
    "DigitalOcean": ["digitalocean", "digital ocean"],
    "Heroku": ["heroku"],
}

IDENTITY_PROVIDERS = {
    "Okta": ["okta"],
    "Google Workspace": ["google workspace", "g suite", "gsuite"],
    "Azure AD": ["azure ad", "azure active directory", "entra"],
    "Auth0": ["auth0"],
    "OneLogin": ["onelogin"],
    "JumpCloud": ["jumpcloud"],
}

TECH_STACK_KEYWORDS = {
    "Stripe": ["stripe"],
    "Salesforce": ["salesforce", "sfdc"],
    "Slack": ["slack"],
    "GitHub": ["github"],
    "GitLab": ["gitlab"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Docker": ["docker"],
    "PostgreSQL": ["postgres", "postgresql"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb"],
    "Redis": ["redis"],
    "Terraform": ["terraform"],
}

REGULATORY_MAP = {
    "HIPAA": ["healthcare", "health", "patient", "medical", "ehr", "phi"],
    "PCI-DSS": ["payment", "credit card", "stripe", "checkout", "pos", "ecommerce"],
    "GDPR": ["european", "eu ", "europe", "gdpr"],
    "CCPA": ["california", "ccpa"],
    "SOC2": ["saas", "software", "cloud", "b2b", "enterprise customers"],
    "FERPA": ["education", "school", "student", "university"],
    "SOX": ["public company", "publicly traded", "sox"],
}

REMOTE_KEYWORDS = {
    "fully_remote": ["fully remote", "100% remote", "all remote", "work from home", "wfh"],
    "hybrid": ["hybrid", "partly remote", "partial remote", "some remote", "flexible"],
    "mostly_onsite": ["mostly onsite", "primarily office", "mainly office"],
    "fully_onsite": ["onsite", "in office", "in-office", "office based"],
}

DATA_SENSITIVITY_MAP = {
    "critical": ["patient", "phi", "financial records", "credit card", "health record", "medical"],
    "high": ["personal data", "pii", "customer data", "employee data", "intellectual property"],
    "medium": ["business data", "internal data", "operational data"],
    "low": ["public data", "marketing data"],
}


def detect_industry(description: str) -> str:
    desc_lower = description.lower()
    scores = {}
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in desc_lower)
        if score > 0:
            scores[industry] = score
    if scores:
        return max(scores, key=scores.get)
    return "technology"  # default


def detect_org_size(description: str) -> Dict[str, Any]:
    desc_lower = description.lower()
    # Look for explicit employee counts
    patterns = [
        r'(\d+)\s*(?:employee|staff|worker|person|people)',
        r'team\s+of\s+(\d+)',
    ]
    for pattern in patterns:
        m = re.search(pattern, desc_lower)
        if m:
            count = int(m.group(1))
            if count <= 10:
                category = "micro"
            elif count <= 50:
                category = "small"
            elif count <= 250:
                category = "medium"
            elif count <= 1000:
                category = "large"
            else:
                category = "enterprise"
            return {"employee_count": count, "category": category}

    # Heuristic from keywords
    if any(kw in desc_lower for kw in ["small", "startup", "early stage"]):
        return {"employee_count": 25, "category": "small"}
    if any(kw in desc_lower for kw in ["medium", "mid-size", "growing"]):
        return {"employee_count": 150, "category": "medium"}
    if any(kw in desc_lower for kw in ["large", "enterprise", "corporation"]):
        return {"employee_count": 500, "category": "large"}
    return {"employee_count": 50, "category": "small"}


def detect_cloud_providers(description: str) -> List[str]:
    desc_lower = description.lower()
    found = []
    for provider, keywords in CLOUD_PROVIDERS.items():
        if any(kw in desc_lower for kw in keywords):
            found.append(provider)
    return found or ["Unknown/On-Premise"]


def detect_identity_providers(description: str) -> List[str]:
    desc_lower = description.lower()
    found = []
    for provider, keywords in IDENTITY_PROVIDERS.items():
        if any(kw in desc_lower for kw in keywords):
            found.append(provider)
    return found or ["Unknown"]


def detect_tech_stack(description: str) -> List[str]:
    desc_lower = description.lower()
    found = []
    for tech, keywords in TECH_STACK_KEYWORDS.items():
        if any(kw in desc_lower for kw in keywords):
            found.append(tech)
    return found


def detect_regulations(description: str, industry: str) -> List[str]:
    desc_lower = (description + " " + industry).lower()
    found = []
    for reg, triggers in REGULATORY_MAP.items():
        if any(t in desc_lower for t in triggers):
            found.append(reg)
    return list(set(found)) or ["SOC2"]


def detect_workforce_distribution(description: str) -> str:
    desc_lower = description.lower()
    for wf_type, keywords in REMOTE_KEYWORDS.items():
        if any(kw in desc_lower for kw in keywords):
            return wf_type
    if "remote" in desc_lower:
        return "hybrid"
    return "hybrid"


def detect_data_sensitivity(description: str, industry: str) -> str:
    combined = (description + " " + industry).lower()
    for level in ["critical", "high", "medium", "low"]:
        if any(kw in combined for kw in DATA_SENSITIVITY_MAP.get(level, [])):
            return level
    return "medium"


def infer_infrastructure_types(cloud_providers: List[str], description: str) -> List[str]:
    infra = []
    desc_lower = description.lower()
    if any(cp not in ["Unknown/On-Premise"] for cp in cloud_providers):
        infra.append("Cloud Infrastructure")
    if any(kw in desc_lower for kw in ["server", "datacenter", "data center", "on-prem", "on premise"]):
        infra.append("On-Premise Servers")
    if any(kw in desc_lower for kw in ["laptop", "workstation", "endpoint", "device", "computer"]):
        infra.append("Employee Endpoints")
    if any(kw in desc_lower for kw in ["mobile", "ios", "android", "phone"]):
        infra.append("Mobile Devices")
    if any(kw in desc_lower for kw in ["vpn", "remote access", "remote desktop", "rdp"]):
        infra.append("VPN/Remote Access")
    if any(kw in desc_lower for kw in ["web app", "website", "portal", "web application"]):
        infra.append("Web Applications")
    if not infra:
        infra = ["Cloud Infrastructure", "Employee Endpoints"]
    return infra


def infer_third_party_dependencies(description: str, tech_stack: List[str]) -> List[str]:
    deps = list(tech_stack)
    desc_lower = description.lower()
    common = {
        "Email Provider": ["email", "gmail", "outlook", "exchange"],
        "Payment Processor": ["payment", "billing", "invoice"],
        "CRM": ["crm", "salesforce", "hubspot", "customers"],
        "Cloud Storage": ["s3", "storage", "file sharing", "dropbox", "google drive"],
        "HR System": ["hr", "human resources", "payroll", "hris"],
        "Collaboration Tools": ["slack", "teams", "zoom", "collaboration"],
    }
    for dep, keywords in common.items():
        if dep not in deps and any(kw in desc_lower for kw in keywords):
            deps.append(dep)
    return deps


def extract_organization_profile(description: str) -> Dict[str, Any]:
    """Main function: extract structured org profile from natural language."""
    industry = detect_industry(description)
    size_info = detect_org_size(description)
    cloud_providers = detect_cloud_providers(description)
    identity_providers = detect_identity_providers(description)
    tech_stack = detect_tech_stack(description)
    regulations = detect_regulations(description, industry)
    workforce = detect_workforce_distribution(description)
    data_sensitivity = detect_data_sensitivity(description, industry)
    infra_types = infer_infrastructure_types(cloud_providers, description)
    third_party = infer_third_party_dependencies(description, tech_stack)

    cloud_type = "unknown"
    if len(cloud_providers) > 1:
        cloud_type = "multi_cloud"
    elif cloud_providers and cloud_providers[0] != "Unknown/On-Premise":
        cloud_type = "single_cloud"
    elif "on-prem" in description.lower() or "on premise" in description.lower():
        cloud_type = "on_premise"
    else:
        cloud_type = "single_cloud"

    return {
        "industry_sector": industry,
        "organization_size": size_info,
        "data_sensitivity_level": data_sensitivity,
        "regulatory_exposure": regulations,
        "technology_stack": tech_stack,
        "cloud_providers": cloud_providers,
        "cloud_deployment_type": cloud_type,
        "identity_providers": identity_providers,
        "infrastructure_types": infra_types,
        "workforce_distribution": workforce,
        "third_party_dependencies": third_party,
        "description_summary": description[:500],
    }
