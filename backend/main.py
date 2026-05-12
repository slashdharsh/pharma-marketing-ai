"""
main.py  –  FastAPI backend for Pharma Marketing AI
Run with: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from drug_fetcher import fetch_all_drug_data
from content_generator import (
    generate_hcp_detail_aid,
    generate_patient_leaflet,
    generate_package_insert_summary,
    generate_clinical_evidence_summary,
)

app = FastAPI(title="Pharma Marketing AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ──────────────────────────────────────────────────

class DrugRequest(BaseModel):
    drug_name: str
    content_type: str   # "hcp_detail_aid" | "patient_leaflet" | "package_insert" | "clinical_evidence" | "all"


class DrugDataResponse(BaseModel):
    drug_name: str
    raw_data: dict
    content: dict


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Pharma Marketing AI API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/drug/raw", response_model=dict)
async def get_raw_drug_data(req: DrugRequest):
    """Fetch raw data from OpenFDA, DailyMed, PubMed — no AI processing."""
    data = await fetch_all_drug_data(req.drug_name)
    if not data.get("fda_label") and not data.get("dailymed"):
        raise HTTPException(status_code=404, detail=f"No data found for '{req.drug_name}'")
    return data


@app.post("/api/drug/generate")
async def generate_content(req: DrugRequest):
    """Fetch drug data + generate marketing content via Groq."""
    # Step 1: Pull from APIs
    raw_data = await fetch_all_drug_data(req.drug_name)

    if not raw_data.get("fda_label") and not raw_data.get("dailymed"):
        raise HTTPException(status_code=404, detail=f"No drug data found for '{req.drug_name}'. Check spelling.")

    # Step 2: Generate content
    content = {}
    ct = req.content_type

    if ct in ("hcp_detail_aid", "all"):
        content["hcp_detail_aid"] = generate_hcp_detail_aid(raw_data)

    if ct in ("patient_leaflet", "all"):
        content["patient_leaflet"] = generate_patient_leaflet(raw_data)

    if ct in ("package_insert", "all"):
        content["package_insert"] = generate_package_insert_summary(raw_data)

    if ct in ("clinical_evidence", "all"):
        content["clinical_evidence"] = generate_clinical_evidence_summary(raw_data)

    return {
        "drug_name": req.drug_name,
        "raw_data":  raw_data,
        "content":   content,
    }


@app.get("/api/drug/search/{drug_name}")
async def quick_search(drug_name: str):
    """Quick lookup — just raw data, no AI generation. Good for autocomplete."""
    return await fetch_all_drug_data(drug_name)
