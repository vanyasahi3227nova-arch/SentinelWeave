# Cyber Risk Analysis Platform — Backend

AI-powered Cyber Risk Analysis and Threat Modeling for SMEs using FAIR methodology, MITRE ATT&CK, and a multi-agent architecture.

---

## Architecture

```
backend/
├── main.py                          # FastAPI application entry point
├── agents/
│   ├── orchestrator.py              # Agent 10: Coordinates all agents
│   ├── organization_profiler.py     # Agent 1: NL → structured org profile
│   ├── asset_inference.py           # Agent 2: Predict asset inventory
│   ├── threat_intelligence.py       # Agent 3: Hybrid RAG threat identification
│   ├── threat_modeling_simulation.py # Agent 4: Kill chain simulation
│   ├── fair_risk_calculation.py     # Agent 5: FAIR LEF × LM risk calculation
│   ├── qualitative_risk_analysis.py # Agent 6: Risk narratives and ratings
│   ├── control_recommendation.py   # Agent 7: NIST CSF / CIS Controls
│   ├── risk_prioritization.py      # Agent 8: Priority scoring
│   └── report_generation.py        # Agent 9: Executive risk report
├── rag/
│   └── hybrid_rag.py               # Vector store + structured retrieval
├── datasets/
│   ├── industry_asset_mapping.json
│   ├── mitre_attack_dataset.json
│   ├── industry_threat_dataset.json
│   ├── fair_baseline_dataset.json
│   └── control_mapping_dataset.json
├── schemas/
│   ├── request_schemas.py
│   └── response_schemas.py
├── utils/
│   └── llm_utils.py                # Rule-based NLP extraction
├── requirements.txt
├── Procfile
├── render.yaml
├── railway.json
├── Dockerfile
└── runtime.txt
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze` | Full risk analysis from org description |
| GET | `/health` | System health check |
| GET | `/agents/status` | Agent readiness status |
| GET | `/docs` | OpenAPI Swagger UI |
| GET | `/redoc` | ReDoc API documentation |

---

## Local Development

### Prerequisites
- Python 3.11+

### Setup and Run

```bash
# Clone or download the backend folder
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --port 8000
```

### Test the API

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "organization_description": "We are a 40-employee healthcare SaaS company hosting patient records in AWS. Employees use laptops and access systems remotely. We use Stripe for payments and Google Workspace."
  }'
```

---

## Deployment on Render.com (Free Tier) — Recommended

### Step 1: Push to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Cyber Risk Analysis Platform"

# Create a new repository on github.com then push
git remote add origin https://github.com/YOUR_USERNAME/cyber-risk-platform.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to **https://render.com** and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select the `cyber-risk-platform` repository
4. Render will auto-detect the `render.yaml` — or configure manually:
   - **Name:** `cyber-risk-platform`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. Click **"Create Web Service"**

### Step 3: Get Your Public URL

After deployment (2-5 minutes), Render provides:

```
https://cyber-risk-platform.onrender.com
```

Your public API endpoints:
```
GET  https://cyber-risk-platform.onrender.com/health
GET  https://cyber-risk-platform.onrender.com/agents/status
POST https://cyber-risk-platform.onrender.com/analyze
GET  https://cyber-risk-platform.onrender.com/docs
```

### Step 4: Test Live API

```bash
curl -X POST https://cyber-risk-platform.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "organization_description": "Healthcare SaaS company using AWS and Okta with 50 employees"
  }'
```

---

## Deployment on Railway.app (Alternative)

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Railway

1. Go to **https://railway.app** and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway detects the `railway.json` automatically
5. Set environment variable: `PORT=8000` (Railway sets this automatically)
6. Click **"Deploy"**

### Public URL

```
https://cyber-risk-platform.up.railway.app
```

---

## Base44 Frontend Integration

Configure Base44 to use the following base URL:

```
Base URL: https://cyber-risk-platform.onrender.com

Primary Endpoint:
POST https://cyber-risk-platform.onrender.com/analyze

Request Body:
{
  "organization_description": "string"
}

Response: Complete JSON risk analysis object
```

---

## Example Full Response Structure

```json
{
  "organization_profile": {
    "industry_sector": "healthcare",
    "organization_size": {"employee_count": 40, "category": "small"},
    "data_sensitivity_level": "critical",
    "regulatory_exposure": ["HIPAA", "PCI-DSS", "SOC2"],
    "cloud_providers": ["AWS"],
    "workforce_distribution": "hybrid"
  },
  "asset_inventory": {
    "assets": [...],
    "summary": {"total_assets": 25, "critical": 6, "high": 8}
  },
  "threat_scenarios": {
    "threat_scenarios": [...],
    "mitre_techniques_identified": [...]
  },
  "attack_simulations": {
    "attack_simulations": [...]
  },
  "fair_risk_analysis": {
    "risk_calculations": [...],
    "summary": {"aggregate_annual_loss_exposure_usd": 3450000}
  },
  "qualitative_risk": {
    "overall_risk_posture": "HIGH RISK - Urgent Remediation Needed",
    "qualitative_assessments": [...]
  },
  "recommended_controls": {
    "immediate_controls": [...],
    "short_term_controls": [...],
    "long_term_controls": [...]
  },
  "prioritized_risks": {
    "prioritized_risk_register": [...]
  },
  "risk_report": {
    "executive_summary": {...},
    "top_risks": [...],
    "risk_roadmap": {...}
  }
}
```

---

## Notes

- **No paid APIs required**: The system uses rule-based NLP extraction + dataset-driven analysis
- **Optional LLM enhancement**: Uncomment `sentence-transformers` in `requirements.txt` for richer embeddings
- **CORS**: Enabled for all origins — compatible with Base44 frontend
- **Free tier**: Works within Render/Railway free tier limits
