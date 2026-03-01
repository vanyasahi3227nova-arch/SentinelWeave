"""
Agent 2: Asset Inference Agent
Predicts likely assets based on organization profile.
"""

from typing import Dict, Any, List
from rag.hybrid_rag import rag


CLOUD_ASSETS = {
    "AWS": ["S3 Buckets", "EC2 Instances", "RDS Databases", "Lambda Functions", "IAM Roles", "CloudWatch", "VPC"],
    "Azure": ["Azure Blob Storage", "Azure VMs", "Azure SQL Database", "Azure AD", "Azure Key Vault"],
    "GCP": ["GCS Buckets", "GCE Instances", "Cloud SQL", "GKE Clusters", "Cloud IAM"],
    "DigitalOcean": ["Droplets", "Spaces (Object Storage)", "Managed Databases"],
    "Heroku": ["Dynos", "Heroku Postgres", "Heroku Redis"],
}

INFRA_ASSETS = {
    "Employee Endpoints": ["Employee Laptops", "Developer Workstations"],
    "Mobile Devices": ["Corporate Mobile Devices", "BYOD Devices"],
    "VPN/Remote Access": ["VPN Gateway", "Remote Desktop Services"],
    "Web Applications": ["Public-Facing Web Application", "Internal Web Portals"],
    "On-Premise Servers": ["On-Prem Application Servers", "On-Prem Database Servers", "File Servers"],
}

IDENTITY_ASSETS = {
    "Okta": ["Okta Identity Provider", "SSO Configuration"],
    "Google Workspace": ["Google Workspace Admin", "Google Drive", "Gmail"],
    "Azure AD": ["Azure Active Directory", "Conditional Access Policies"],
    "Auth0": ["Auth0 Tenant"],
    "JumpCloud": ["JumpCloud Directory"],
}

ASSET_CRITICALITY = {
    "critical": ["Database", "EHR", "Patient", "Financial", "Payment", "Core Banking", "Records", "PHI", "PII"],
    "high": ["API", "Application", "Portal", "Identity", "IAM", "Admin", "Source Code"],
    "medium": ["Storage", "Workstation", "Laptop", "VM", "Container", "Monitoring"],
    "low": ["Backup", "Log", "Archive", "Static", "CDN"],
}


def classify_asset_criticality(asset_name: str) -> str:
    for level, keywords in ASSET_CRITICALITY.items():
        if any(kw.lower() in asset_name.lower() for kw in keywords):
            return level
    return "medium"


class AssetInferenceAgent:
    """
    Builds asset inventory based on industry profile, cloud providers,
    infrastructure types, and identity providers.
    """

    def run(self, organization_profile: Dict[str, Any]) -> Dict[str, Any]:
        profile = organization_profile.get("data", organization_profile)
        industry = profile.get("industry_sector", "general")
        cloud_providers = profile.get("cloud_providers", [])
        infra_types = profile.get("infrastructure_types", [])
        identity_providers = profile.get("identity_providers", [])

        assets = []

        # Industry-specific assets from structured lookup
        industry_data = rag.get_industry_assets(industry)
        for asset_name in industry_data.get("assets", []):
            assets.append({
                "name": asset_name,
                "source": "industry_baseline",
                "criticality": classify_asset_criticality(asset_name),
                "asset_type": "application",
            })

        # Cloud provider assets
        for cp in cloud_providers:
            for asset_name in CLOUD_ASSETS.get(cp, []):
                assets.append({
                    "name": asset_name,
                    "source": f"cloud_provider:{cp}",
                    "criticality": classify_asset_criticality(asset_name),
                    "asset_type": "cloud_resource",
                })

        # Infrastructure assets
        for infra in infra_types:
            for asset_name in INFRA_ASSETS.get(infra, []):
                assets.append({
                    "name": asset_name,
                    "source": f"infrastructure:{infra}",
                    "criticality": classify_asset_criticality(asset_name),
                    "asset_type": "infrastructure",
                })

        # Identity provider assets
        for idp in identity_providers:
            for asset_name in IDENTITY_ASSETS.get(idp, []):
                assets.append({
                    "name": asset_name,
                    "source": f"identity_provider:{idp}",
                    "criticality": classify_asset_criticality(asset_name),
                    "asset_type": "identity_system",
                })

        # Deduplicate by name
        seen = set()
        unique_assets = []
        for a in assets:
            if a["name"] not in seen:
                seen.add(a["name"])
                unique_assets.append(a)

        # Summary counts
        summary = {
            "total_assets": len(unique_assets),
            "critical": sum(1 for a in unique_assets if a["criticality"] == "critical"),
            "high": sum(1 for a in unique_assets if a["criticality"] == "high"),
            "medium": sum(1 for a in unique_assets if a["criticality"] == "medium"),
            "low": sum(1 for a in unique_assets if a["criticality"] == "low"),
        }

        return {
            "status": "success",
            "agent": "asset_inference",
            "data": {
                "assets": unique_assets,
                "summary": summary,
                "data_types": industry_data.get("data_types", []),
                "regulations_inferred": industry_data.get("regulations", []),
            }
        }
