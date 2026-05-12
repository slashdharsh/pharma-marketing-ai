"""
content_generator.py
Uses Groq (free tier) to turn raw drug data into structured
pharma marketing content. Drug data is trimmed before sending
to stay within the 12,000 TPM free tier limit.
"""

import os, re, json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL  = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a senior pharma medical writer with 15+ years experience.
Write accurate, regulatory-compliant content based ONLY on the drug data provided.
Never invent clinical claims. Output must be valid JSON matching exactly the schema requested."""


# ── Data trimmer — keeps prompts under ~6000 tokens ──────────────────────────

def _trim(text: str | None, max_chars: int = 600) -> str:
    """Truncate long text fields so they don't blow up the prompt."""
    if not text:
        return ""
    return text[:max_chars].rsplit(" ", 1)[0] + "…" if len(text) > max_chars else text


def _slim_drug_data(drug_data: dict) -> dict:
    """Return a compact version of drug_data safe to send to Groq."""
    fda = drug_data.get("fda_label", {})
    pubmed = drug_data.get("pubmed", [])[:3]   # max 3 papers

    return {
        "drug_name":   drug_data.get("drug_name", ""),
        "brand_name":  fda.get("brand_name", ""),
        "generic_name":fda.get("generic_name", ""),
        "drug_class":  fda.get("drug_class", ""),
        "route":       fda.get("route", ""),
        "manufacturer":fda.get("manufacturer", ""),
        "indications":          _trim(fda.get("indications"), 500),
        "mechanism_of_action":  _trim(fda.get("mechanism_of_action"), 500),
        "dosage":               _trim(fda.get("dosage"), 400),
        "warnings":             _trim(fda.get("warnings"), 400),
        "contraindications":    _trim(fda.get("contraindications"), 300),
        "adverse_reactions":    _trim(fda.get("adverse_reactions"), 400),
        "pharmacokinetics":     _trim(fda.get("pharmacokinetics"), 300),
        "drug_interactions":    _trim(fda.get("drug_interactions"), 300),
        "clinical_studies":     _trim(fda.get("clinical_studies"), 400),
        "how_supplied":         _trim(fda.get("how_supplied"), 200),
        "pubmed_titles": [p.get("title","") for p in pubmed],
        "dailymed_url":  drug_data.get("dailymed", {}).get("url", ""),
        "adverse_events_top5": [
            e.get("term","") for e in drug_data.get("adverse_events", [])[:5]
        ],
    }


# ── Groq call ─────────────────────────────────────────────────────────────────

def _call_groq(user_prompt: str, max_tokens: int = 1500) -> str:
    chat = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return chat.choices[0].message.content


# ── Generators ────────────────────────────────────────────────────────────────

def generate_hcp_detail_aid(drug_data: dict) -> dict:
    d = _slim_drug_data(drug_data)
    prompt = f"""Generate a concise HCP Detail Aid. Return ONLY valid JSON:
{{
  "headline": "bold marketing headline",
  "tagline": "short 1-line sub-headline",
  "brand_name": "{d['brand_name']}",
  "generic_name": "{d['generic_name']}",
  "drug_class": "{d['drug_class']}",
  "indication": "approved indication (1-2 sentences)",
  "mechanism_of_action": "plain-language MOA (2-3 sentences)",
  "key_efficacy_points": ["point 1", "point 2", "point 3"],
  "dosing_summary": "simple dosing text",
  "safety_highlights": ["key warning 1", "key warning 2"],
  "patient_selection": "ideal patient profile (2-3 sentences)",
  "references": ["ref 1"]
}}

DRUG DATA:
{json.dumps(d, indent=2)}
"""
    return _safe_json(_call_groq(prompt))


def generate_patient_leaflet(drug_data: dict) -> dict:
    d = _slim_drug_data(drug_data)
    prompt = f"""Write a Patient Information Leaflet in plain language (6th grade level).
Return ONLY valid JSON:
{{
  "title": "Patient Guide: {d['brand_name'] or d['generic_name']}",
  "what_is_it": "What is this medicine (2-3 sentences)",
  "how_it_works": "How it works in simple terms (2-3 sentences)",
  "how_to_take": "How to take it",
  "what_to_expect": "What patient might feel (2 sentences)",
  "side_effects": ["side effect 1", "side effect 2", "side effect 3"],
  "when_to_call_doctor": ["warning sign 1", "warning sign 2"],
  "storage": "storage instructions",
  "important_reminders": ["reminder 1", "reminder 2"]
}}

DRUG DATA:
{json.dumps(d, indent=2)}
"""
    return _safe_json(_call_groq(prompt))


def generate_package_insert_summary(drug_data: dict) -> dict:
    d = _slim_drug_data(drug_data)
    prompt = f"""Generate a Package Insert Summary for HCPs. Return ONLY valid JSON:
{{
  "brand_name": "{d['brand_name']}",
  "generic_name": "{d['generic_name']}",
  "drug_class": "{d['drug_class']}",
  "indications_and_usage": "full indication",
  "dosage_and_administration": "dosing summary",
  "contraindications": ["contraindication 1", "contraindication 2"],
  "warnings_and_precautions": ["warning 1", "warning 2"],
  "adverse_reactions": {{
    "common": ["ae 1", "ae 2"],
    "serious": ["serious ae 1"]
  }},
  "drug_interactions": ["interaction 1", "interaction 2"],
  "use_in_specific_populations": {{
    "pregnancy": "...",
    "pediatric": "...",
    "geriatric": "...",
    "renal_impairment": "..."
  }},
  "mechanism_of_action": "...",
  "pharmacokinetics": "ADME summary",
  "clinical_trials": "key trial results",
  "how_supplied": "..."
}}

DRUG DATA:
{json.dumps(d, indent=2)}
"""
    return _safe_json(_call_groq(prompt, max_tokens=1800))


def generate_clinical_evidence_summary(drug_data: dict) -> dict:
    d = _slim_drug_data(drug_data)
    prompt = f"""Generate a Clinical Evidence Summary. Return ONLY valid JSON:
{{
  "drug_name": "{d['drug_name']}",
  "evidence_overview": "2-3 sentence overview",
  "key_trials": [
    {{
      "trial_name": "...",
      "design": "RCT / meta-analysis / etc",
      "n_patients": "...",
      "primary_endpoint": "...",
      "key_result": "...",
      "reference": "..."
    }}
  ],
  "efficacy_highlights": ["highlight 1", "highlight 2", "highlight 3"],
  "safety_profile": "2-3 sentence safety summary",
  "place_in_therapy": "where this drug fits vs alternatives (2-3 sentences)"
}}

DRUG DATA:
{json.dumps(d, indent=2)}

PUBMED TITLES:
{chr(10).join(d['pubmed_titles'])}
"""
    return _safe_json(_call_groq(prompt))


# ── Utility ───────────────────────────────────────────────────────────────────

def _safe_json(raw: str) -> dict:
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw_text": raw, "parse_error": True}
