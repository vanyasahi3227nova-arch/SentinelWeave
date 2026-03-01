"""
Hybrid RAG Pipeline
Uses sentence-transformers for embeddings + FAISS for vector search
Plus structured JSON retrieval for deterministic lookups
"""

import json
import os
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path

DATASETS_DIR = Path(__file__).parent.parent / "datasets"


# ─── Lightweight embedding using hashing (no heavy ML models needed for deployment) ───
def simple_embed(text: str, dim: int = 128) -> np.ndarray:
    """
    Fast deterministic embedding via character n-gram hashing.
    Falls back to this if sentence-transformers is unavailable.
    """
    vec = np.zeros(dim)
    text = text.lower()
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        idx = hash(trigram) % dim
        vec[idx] += 1.0
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


try:
    from sentence_transformers import SentenceTransformer
    _model = SentenceTransformer("all-MiniLM-L6-v2")
    def get_embedding(text: str) -> np.ndarray:
        return _model.encode(text, normalize_embeddings=True)
    EMBEDDINGS_BACKEND = "sentence-transformers"
except Exception:
    def get_embedding(text: str) -> np.ndarray:
        return simple_embed(text)
    EMBEDDINGS_BACKEND = "simple-hash"


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


class VectorStore:
    """In-memory FAISS-style vector store."""
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: List[np.ndarray] = []

    def add(self, doc: Dict[str, Any], text_key: str = "text"):
        text = doc.get(text_key, "") or json.dumps(doc)
        emb = get_embedding(text)
        self.documents.append(doc)
        self.embeddings.append(emb)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.embeddings:
            return []
        q_emb = get_embedding(query)
        scores = [cosine_similarity(q_emb, e) for e in self.embeddings]
        ranked = sorted(zip(scores, self.documents), key=lambda x: x[0], reverse=True)
        return [doc for _, doc in ranked[:top_k]]


# ─── Build vector stores from datasets ───
def _load_json(filename: str) -> Any:
    path = DATASETS_DIR / filename
    with open(path) as f:
        return json.load(f)


class HybridRAG:
    """Combines vector search and structured lookup."""

    def __init__(self):
        self.mitre_store = VectorStore()
        self.threat_store = VectorStore()
        self.industry_asset_data: Dict = {}
        self.fair_data: Dict = {}
        self.control_data: Dict = {}
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return

        # Load MITRE ATT&CK into vector store
        mitre = _load_json("mitre_attack_dataset.json")
        for tech in mitre.get("techniques", []):
            tech["text"] = f"{tech['name']} {tech['description']} tactic:{tech['tactic']}"
            self.mitre_store.add(tech)

        # Load industry threat dataset into vector store
        industry_threats = _load_json("industry_threat_dataset.json")
        for sector, data in industry_threats.items():
            doc = {
                "sector": sector,
                "top_threats": data["top_threats"],
                "threat_actors": data["threat_actors"],
                "avg_breach_cost": data["avg_breach_cost"],
                "breach_probability_per_year": data["breach_probability_per_year"],
                "text": f"{sector} threats: {' '.join(data['top_threats'])}"
            }
            self.threat_store.add(doc)

        # Load structured datasets
        self.industry_asset_data = _load_json("industry_asset_mapping.json")
        self.fair_data = _load_json("fair_baseline_dataset.json")
        self.control_data = _load_json("control_mapping_dataset.json")

        self._initialized = True

    # ─── Structured retrieval ───
    def get_industry_assets(self, industry: str) -> Dict:
        self.initialize()
        industry_lower = industry.lower()
        for key in self.industry_asset_data:
            if key in industry_lower or industry_lower in key:
                return self.industry_asset_data[key]
        return self.industry_asset_data.get("general", {})

    def get_fair_baseline(self) -> Dict:
        self.initialize()
        return self.fair_data

    def get_controls(self, threat_categories: Optional[List[str]] = None) -> List[Dict]:
        self.initialize()
        controls = self.control_data.get("controls", [])
        if not threat_categories:
            return controls
        relevant = []
        for ctrl in controls:
            ctrl_cats = ctrl.get("threat_categories", [])
            if "all" in ctrl_cats:
                relevant.append(ctrl)
            elif any(tc.lower() in [c.lower() for c in ctrl_cats] for tc in threat_categories):
                relevant.append(ctrl)
        return relevant or controls[:8]

    # ─── Vector retrieval ───
    def search_mitre_techniques(self, query: str, top_k: int = 5) -> List[Dict]:
        self.initialize()
        return self.mitre_store.search(query, top_k)

    def search_industry_threats(self, query: str, top_k: int = 3) -> List[Dict]:
        self.initialize()
        return self.threat_store.search(query, top_k)

    def get_embedding_backend(self) -> str:
        return EMBEDDINGS_BACKEND


# Global singleton
rag = HybridRAG()
