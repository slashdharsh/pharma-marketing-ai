"""
drug_fetcher.py
Pulls structured drug data from free, no-key APIs:
  - OpenFDA  (drug labels, adverse events)
  - DailyMed (full prescribing info / SPL)
  - PubMed   (clinical evidence abstracts)
"""

import httpx
import asyncio
from typing import Optional

OPENFDA_BASE   = "https://api.fda.gov/drug"
DAILYMED_BASE  = "https://dailymed.nlm.nih.gov/dailymed/services/v2"
PUBMED_BASE    = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


# ── OpenFDA ──────────────────────────────────────────────────────────────────

async def fetch_openfda_label(drug_name: str) -> dict:
    """Fetch the full drug label from OpenFDA (indications, dosing, warnings, MOA)."""
    url = f"{OPENFDA_BASE}/label.json"
    params = {"search": f'openfda.brand_name:"{drug_name}" OR openfda.generic_name:"{drug_name}"', "limit": 1}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                return _parse_fda_label(results[0])
    # Fallback: broader search
    params["search"] = f'"{drug_name}"'
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                return _parse_fda_label(results[0])
    return {}


def _parse_fda_label(raw: dict) -> dict:
    def first(key):
        val = raw.get(key, [])
        return val[0] if val else None

    openfda = raw.get("openfda", {})
    return {
        "brand_name":           (openfda.get("brand_name", [None])[0]),
        "generic_name":         (openfda.get("generic_name", [None])[0]),
        "manufacturer":         (openfda.get("manufacturer_name", [None])[0]),
        "drug_class":           (openfda.get("pharm_class_epc", [None])[0]),
        "route":                (openfda.get("route", [None])[0]),
        "indications":          first("indications_and_usage"),
        "dosage":               first("dosage_and_administration"),
        "warnings":             first("warnings_and_cautions") or first("warnings"),
        "contraindications":    first("contraindications"),
        "adverse_reactions":    first("adverse_reactions"),
        "mechanism_of_action":  first("mechanism_of_action"),
        "pharmacokinetics":     first("pharmacokinetics"),
        "drug_interactions":    first("drug_interactions"),
        "clinical_studies":     first("clinical_studies"),
        "how_supplied":         first("how_supplied"),
    }


async def fetch_openfda_adverse_events(drug_name: str, limit: int = 5) -> list[dict]:
    """Top adverse event reports from FAERS."""
    url = f"{OPENFDA_BASE}/event.json"
    params = {
        "search": f'patient.drug.medicinalproduct:"{drug_name}"',
        "count": "patient.reaction.reactionmeddrapt.exact",
        "limit": limit,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)
        if resp.status_code == 200:
            return resp.json().get("results", [])
    return []


# ── DailyMed ─────────────────────────────────────────────────────────────────

async def fetch_dailymed_info(drug_name: str) -> dict:
    """Search DailyMed and return SPL set-id + basic metadata."""
    search_url = f"{DAILYMED_BASE}/spls.json"
    params = {"drug_name": drug_name, "pagesize": 1}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(search_url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            spls = data.get("data", [])
            if spls:
                spl = spls[0]
                return {
                    "set_id":    spl.get("setid"),
                    "title":     spl.get("title"),
                    "published": spl.get("published_date"),
                    "url":       f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={spl.get('setid')}",
                }
    return {}


# ── PubMed ────────────────────────────────────────────────────────────────────

async def fetch_pubmed_abstracts(drug_name: str, max_results: int = 5) -> list[dict]:
    """Return top PubMed abstracts for the drug (clinical trials / RCTs preferred)."""
    search_url = f"{PUBMED_BASE}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": f"{drug_name}[Title/Abstract] AND (clinical trial[pt] OR randomized[tiab])",
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance",
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(search_url, params=params)
        if resp.status_code != 200:
            return []
        ids = resp.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []

        # Fetch summaries
        summary_url = f"{PUBMED_BASE}/esummary.fcgi"
        s_params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
        s_resp = await client.get(summary_url, params=s_params)
        if s_resp.status_code != 200:
            return []

        uids = s_resp.json().get("result", {})
        articles = []
        for uid in ids:
            art = uids.get(uid, {})
            articles.append({
                "pmid":    uid,
                "title":   art.get("title", ""),
                "authors": ", ".join(a.get("name", "") for a in art.get("authors", [])[:3]),
                "journal": art.get("fulljournalname", ""),
                "year":    art.get("pubdate", "")[:4],
                "url":     f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
            })
        return articles


# ── Master fetch ──────────────────────────────────────────────────────────────

async def fetch_all_drug_data(drug_name: str) -> dict:
    """Run all fetchers in parallel and return a unified drug data dict."""
    fda_label, dailymed, pubmed, adverse = await asyncio.gather(
        fetch_openfda_label(drug_name),
        fetch_dailymed_info(drug_name),
        fetch_pubmed_abstracts(drug_name),
        fetch_openfda_adverse_events(drug_name),
    )
    return {
        "drug_name":     drug_name,
        "fda_label":     fda_label,
        "dailymed":      dailymed,
        "pubmed":        pubmed,
        "adverse_events": adverse,
    }
