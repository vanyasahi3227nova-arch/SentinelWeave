from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    organization_description: str

    class Config:
        json_schema_extra = {
            "example": {
                "organization_description": "We are a 40-employee healthcare SaaS company hosting patient records in AWS. Employees use laptops and access systems remotely. We use Stripe for payments and Google Workspace."
            }
        }
