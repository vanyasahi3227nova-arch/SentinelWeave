"""
Agent 1: Organization Profiler Agent
Converts natural language description into structured organization profile.
"""

from utils.llm_utils import extract_organization_profile
from typing import Dict, Any


class OrganizationProfilerAgent:
    """
    Parses natural language SME description and produces a structured
    organization profile including industry, size, regulatory exposure, etc.
    """

    def run(self, description: str) -> Dict[str, Any]:
        profile = extract_organization_profile(description)
        return {
            "status": "success",
            "agent": "organization_profiler",
            "data": profile
        }
