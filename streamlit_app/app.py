"""
app.py  —  Pharma Marketing AI · Streamlit Edition
Run locally:   streamlit run app.py
Deploy:        streamlit.io/cloud (free)
"""

import asyncio
import streamlit as st
from drug_fetcher import fetch_all_drug_data
from content_generator import (
    generate_hcp_detail_aid,
    generate_patient_leaflet,
    generate_package_insert_summary,
    generate_clinical_evidence_summary,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pharma Marketing AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #015a9a 0%, #0c90e1 60%, #00c896 100%);
    padding: 2.2rem 2.5rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 1.5rem;
}
.hero-banner h1 {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 2.4rem;
    margin: 0 0 0.3rem 0;
    font-weight: 400;
}
.hero-banner p { margin: 0; opacity: 0.85; font-size: 0.9rem; }

/* Drug result banner */
.drug-banner {
    background: linear-gradient(135deg, #015a9a, #0c90e1);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 1.2rem;
}
.drug-banner h2 {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 2rem;
    margin: 0 0 0.2rem 0;
    font-weight: 400;
}
.drug-banner .sub { opacity: 0.75; font-size: 0.85rem; margin: 0; }

/* Cards */
.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.card h4 {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin: 0 0 0.7rem 0;
}
.card p, .card li { font-size: 0.9rem; color: #374151; line-height: 1.6; margin: 0; }
.card ul { padding-left: 1.2rem; margin: 0; }
.card li { margin-bottom: 0.3rem; }

/* Accent card */
.card-accent { border-color: #00c896; }
.card-warn   { background: #fffbeb; border-color: #fbbf24; }
.card-danger { background: #fef2f2; border-color: #fca5a5; }
.card-info   { background: #eff6ff; border-color: #93c5fd; }
.card-dark   { background: #1e293b; border-color: #334155; color: white; }
.card-dark h4 { color: #94a3b8; }
.card-dark p, .card-dark li { color: #e2e8f0; }

/* Badges */
.badge {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.15rem 0.2rem 0.15rem 0;
}
.badge-blue   { background: #dbeafe; color: #1d4ed8; }
.badge-amber  { background: #fef3c7; color: #92400e; }
.badge-red    { background: #fee2e2; color: #b91c1c; }
.badge-green  { background: #dcfce7; color: #166534; }
.badge-purple { background: #ede9fe; color: #6d28d9; }
.badge-teal   { background: #ccfbf1; color: #0f766e; }

/* Trial card */
.trial-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
}
.trial-card h5 { font-size: 0.9rem; font-weight: 600; margin: 0 0 0.4rem 0; color: #1e293b; }
.trial-card .meta { font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.6rem; }
.trial-result { color: #059669; font-weight: 600; font-size: 0.85rem; }

/* Source pills */
.source-pill {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: white;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    font-size: 0.72rem;
    margin-right: 0.4rem;
}

/* Divider */
hr { border: none; border-top: 1px solid #e2e8f0; margin: 1rem 0; }

/* Hide streamlit branding in content area */
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Free key at console.groq.com"
    )
    if groq_key:
        import os
        os.environ["GROQ_API_KEY"] = groq_key
        st.success("✓ Key set")
    else:
        st.info("Enter your free Groq key above to enable AI generation.\nGet one at console.groq.com")

    st.markdown("---")
    st.markdown("### 📚 Data Sources")
    st.markdown("""
- 🏛️ **OpenFDA** — Labels, adverse events
- 💊 **DailyMed** — Full prescribing info
- 🔬 **PubMed** — Clinical evidence
- 🤖 **Groq AI** — Content generation
    """)

    st.markdown("---")
    st.markdown("### 💡 Example Drugs")
    examples = ["Metformin", "Atorvastatin", "Lisinopril", "Omeprazole", "Sertraline", "Amoxicillin", "Ibuprofen"]
    for ex in examples:
        if st.button(ex, use_container_width=True, key=f"ex_{ex}"):
            st.session_state["drug_input"] = ex
            st.session_state["trigger_search"] = True

    st.markdown("---")
    st.caption("Pharma Marketing AI · Phase 1\nPowered by Groq · OpenFDA · PubMed")


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>💊 Pharma Marketing AI</h1>
    <p>Enter a drug name to generate HCP Detail Aids · Patient Leaflets · Package Inserts · Clinical Evidence Summaries</p>
    <br/>
    <span class="source-pill">OpenFDA</span>
    <span class="source-pill">DailyMed</span>
    <span class="source-pill">PubMed</span>
    <span class="source-pill">Groq AI</span>
</div>
""", unsafe_allow_html=True)


# ── Search bar ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    default_val = st.session_state.get("drug_input", "")
    drug_input = st.text_input(
        "Drug name",
        value=default_val,
        placeholder="e.g. Metformin, Atorvastatin, Lisinopril…",
        label_visibility="collapsed",
    )
with col2:
    search_btn = st.button("🔍 Generate", use_container_width=True, type="primary")

trigger = search_btn or st.session_state.get("trigger_search", False)
if st.session_state.get("trigger_search"):
    st.session_state["trigger_search"] = False
    drug_input = st.session_state.get("drug_input", drug_input)


# ── Main logic ────────────────────────────────────────────────────────────────
if trigger and drug_input.strip():
    if not groq_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar first. Get one free at console.groq.com")
        st.stop()

    drug_name = drug_input.strip()

    # Step 1: Fetch raw data
    with st.spinner(f"🔍 Fetching data for **{drug_name}** from FDA · DailyMed · PubMed…"):
        try:
            raw_data = asyncio.run(fetch_all_drug_data(drug_name))
        except Exception as e:
            st.error(f"Data fetch error: {e}")
            st.stop()

    fda = raw_data.get("fda_label", {})
    if not fda and not raw_data.get("dailymed"):
        st.error(f"❌ No data found for **{drug_name}**. Check the spelling or try the generic/brand name.")
        st.stop()

    # Step 2: Generate all content
    with st.spinner("🤖 Generating content with Groq AI…"):
        try:
            hcp    = generate_hcp_detail_aid(raw_data)
            pat    = generate_patient_leaflet(raw_data)
            pi     = generate_package_insert_summary(raw_data)
            clin   = generate_clinical_evidence_summary(raw_data)
        except Exception as e:
            st.error(f"AI generation error: {e}")
            st.stop()

    # ── Drug banner ──
    brand   = fda.get("brand_name") or drug_name.title()
    generic = fda.get("generic_name") or ""
    dclass  = fda.get("drug_class") or ""
    pubmed_n = len(raw_data.get("pubmed", []))

    st.markdown(f"""
    <div class="drug-banner">
        <h2>{brand}</h2>
        <p class="sub">{generic} · {dclass}</p>
        <br/>
        <span class="source-pill">✓ FDA Label</span>
        <span class="source-pill">✓ DailyMed</span>
        <span class="source-pill">✓ {pubmed_n} PubMed papers</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🩺 HCP Detail Aid",
        "💊 Patient Leaflet",
        "📄 Package Insert",
        "🔬 Clinical Evidence",
        "🗄️ Raw Data",
    ])

    # ════════════════════════════════════════════════════════════════
    # TAB 1 — HCP DETAIL AID
    # ════════════════════════════════════════════════════════════════
    with tab1:
        if hcp.get("parse_error"):
            st.code(hcp.get("raw_text", ""), language="text")
        else:
            # Hero headline
            st.markdown(f"""
            <div class="card card-accent" style="background:linear-gradient(135deg,#015a9a,#0c90e1);border:none;color:white;">
                <h4 style="color:rgba(255,255,255,0.6);">{hcp.get('drug_class','')}</h4>
                <div style="font-family:'DM Serif Display',Georgia,serif;font-size:2rem;margin-bottom:0.3rem;">{hcp.get('brand_name') or hcp.get('generic_name','')}</div>
                <div style="opacity:0.8;font-size:1rem;margin-bottom:0.8rem;">{hcp.get('generic_name','')}</div>
                <div style="background:rgba(255,255,255,0.12);border-radius:8px;padding:0.8rem 1rem;font-style:italic;font-size:1rem;">
                    "{hcp.get('headline','')}"
                </div>
                <div style="opacity:0.75;font-size:0.85rem;margin-top:0.5rem;">{hcp.get('tagline','')}</div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""<div class="card">
                    <h4>✦ Indication</h4>
                    <p>{hcp.get('indication','')}</p>
                </div>""", unsafe_allow_html=True)

            with c2:
                st.markdown(f"""<div class="card">
                    <h4>⚡ Mechanism of Action</h4>
                    <p>{hcp.get('mechanism_of_action','')}</p>
                </div>""", unsafe_allow_html=True)

            # Efficacy points
            pts = hcp.get("key_efficacy_points", [])
            pts_html = "".join(f'<li>{p}</li>' for p in pts)
            st.markdown(f"""<div class="card card-accent">
                <h4>✓ Key Efficacy Points</h4>
                <ul>{pts_html}</ul>
            </div>""", unsafe_allow_html=True)

            c3, c4 = st.columns(2)
            with c3:
                st.markdown(f"""<div class="card">
                    <h4>💉 Dosing Summary</h4>
                    <p style="white-space:pre-line;">{hcp.get('dosing_summary','')}</p>
                </div>""", unsafe_allow_html=True)
            with c4:
                st.markdown(f"""<div class="card">
                    <h4>👥 Patient Selection</h4>
                    <p>{hcp.get('patient_selection','')}</p>
                </div>""", unsafe_allow_html=True)

            safety = hcp.get("safety_highlights", [])
            badges = "".join(f'<span class="badge badge-amber">{s}</span>' for s in safety)
            st.markdown(f"""<div class="card card-warn">
                <h4>⚠️ Safety Highlights</h4>
                <div>{badges}</div>
            </div>""", unsafe_allow_html=True)

            refs = hcp.get("references", [])
            if refs:
                ref_html = "".join(f"<li>{r}</li>" for r in refs)
                st.markdown(f"""<div class="card" style="font-size:0.78rem;color:#64748b;">
                    <h4>References</h4>
                    <ul style="font-size:0.78rem;color:#64748b;">{ref_html}</ul>
                </div>""", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════
    # TAB 2 — PATIENT LEAFLET
    # ════════════════════════════════════════════════════════════════
    with tab2:
        if pat.get("parse_error"):
            st.code(pat.get("raw_text", ""), language="text")
        else:
            st.markdown(f"""
            <div class="card" style="background:linear-gradient(135deg,#00c896,#0891b2);border:none;color:white;">
                <h4 style="color:rgba(255,255,255,0.6);">Patient Information</h4>
                <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;">{pat.get('title','')}</div>
            </div>""", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""<div class="card card-info">
                    <h4>ℹ️ What is this medicine?</h4>
                    <p>{pat.get('what_is_it','')}</p>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="card card-info">
                    <h4>❤️ How does it work?</h4>
                    <p>{pat.get('how_it_works','')}</p>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="card">
                <h4>📋 How to take it</h4>
                <p style="white-space:pre-line;">{pat.get('how_to_take','')}</p>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="card">
                <h4>🌡️ What you might feel</h4>
                <p>{pat.get('what_to_expect','')}</p>
            </div>""", unsafe_allow_html=True)

            c3, c4 = st.columns(2)
            with c3:
                se_badges = "".join(f'<span class="badge badge-amber">{s}</span>' for s in pat.get("side_effects",[]))
                st.markdown(f"""<div class="card card-warn">
                    <h4>⚠️ Possible Side Effects</h4>
                    <div>{se_badges}</div>
                </div>""", unsafe_allow_html=True)
            with c4:
                dr_badges = "".join(f'<span class="badge badge-red">{s}</span>' for s in pat.get("when_to_call_doctor",[]))
                st.markdown(f"""<div class="card card-danger">
                    <h4>🚨 When to Call Your Doctor</h4>
                    <div>{dr_badges}</div>
                </div>""", unsafe_allow_html=True)

            c5, c6 = st.columns(2)
            with c5:
                st.markdown(f"""<div class="card">
                    <h4>🏠 Storage</h4>
                    <p>{pat.get('storage','')}</p>
                </div>""", unsafe_allow_html=True)
            with c6:
                rem = "".join(f'<span class="badge badge-teal">{r}</span>' for r in pat.get("important_reminders",[]))
                st.markdown(f"""<div class="card">
                    <h4>📌 Important Reminders</h4>
                    <div>{rem}</div>
                </div>""", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════
    # TAB 3 — PACKAGE INSERT
    # ════════════════════════════════════════════════════════════════
    with tab3:
        if pi.get("parse_error"):
            st.code(pi.get("raw_text", ""), language="text")
        else:
            st.markdown(f"""
            <div class="card card-dark">
                <h4>Package Insert / Prescribing Information</h4>
                <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;color:white;">{pi.get('brand_name','')}</div>
                <div style="color:#94a3b8;font-size:1rem;">({pi.get('generic_name','')}) · {pi.get('drug_class','')}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="card">
                <h4>Indications and Usage</h4>
                <p>{pi.get('indications_and_usage','')}</p>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="card">
                <h4>Dosage and Administration</h4>
                <p style="white-space:pre-line;">{pi.get('dosage_and_administration','')}</p>
            </div>""", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                ci_b = "".join(f'<span class="badge badge-red">{x}</span>' for x in pi.get("contraindications",[]))
                st.markdown(f"""<div class="card card-danger">
                    <h4>🚫 Contraindications</h4>
                    <div>{ci_b}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                wp_b = "".join(f'<span class="badge badge-amber">{x}</span>' for x in pi.get("warnings_and_precautions",[]))
                st.markdown(f"""<div class="card card-warn">
                    <h4>⚠️ Warnings & Precautions</h4>
                    <div>{wp_b}</div>
                </div>""", unsafe_allow_html=True)

            ar = pi.get("adverse_reactions", {})
            common_b  = "".join(f'<span class="badge badge-blue">{x}</span>' for x in ar.get("common",[]))
            serious_b = "".join(f'<span class="badge badge-red">{x}</span>'  for x in ar.get("serious",[]))
            st.markdown(f"""<div class="card">
                <h4>Adverse Reactions</h4>
                <p style="font-size:0.75rem;color:#64748b;margin-bottom:0.4rem;">COMMON</p>
                <div style="margin-bottom:0.6rem;">{common_b}</div>
                <p style="font-size:0.75rem;color:#ef4444;margin-bottom:0.4rem;">SERIOUS</p>
                <div>{serious_b}</div>
            </div>""", unsafe_allow_html=True)

            di_b = "".join(f'<span class="badge badge-purple">{x}</span>' for x in pi.get("drug_interactions",[]))
            st.markdown(f"""<div class="card">
                <h4>Drug Interactions</h4>
                <div>{di_b}</div>
            </div>""", unsafe_allow_html=True)

            pops = pi.get("use_in_specific_populations", {})
            if pops:
                pop_html = "".join(
                    f'<div style="padding:0.7rem;background:#f8fafc;border-radius:8px;margin-bottom:0.5rem;">'
                    f'<strong style="font-size:0.8rem;text-transform:capitalize;">{k.replace("_"," ")}</strong>'
                    f'<p style="margin:0.3rem 0 0 0;font-size:0.85rem;color:#475569;">{v}</p></div>'
                    for k, v in pops.items()
                )
                st.markdown(f"""<div class="card">
                    <h4>Use in Specific Populations</h4>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">{pop_html}</div>
                </div>""", unsafe_allow_html=True)

            c3, c4 = st.columns(2)
            with c3:
                st.markdown(f"""<div class="card">
                    <h4>Mechanism of Action</h4>
                    <p>{pi.get('mechanism_of_action','')}</p>
                </div>""", unsafe_allow_html=True)
            with c4:
                st.markdown(f"""<div class="card">
                    <h4>Pharmacokinetics</h4>
                    <p>{pi.get('pharmacokinetics','')}</p>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="card">
                <h4>Clinical Trials</h4>
                <p>{pi.get('clinical_trials','')}</p>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="card">
                <h4>How Supplied</h4>
                <p>{pi.get('how_supplied','')}</p>
            </div>""", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════
    # TAB 4 — CLINICAL EVIDENCE
    # ════════════════════════════════════════════════════════════════
    with tab4:
        if clin.get("parse_error"):
            st.code(clin.get("raw_text", ""), language="text")
        else:
            st.markdown(f"""
            <div class="card" style="background:linear-gradient(135deg,#4f46e5,#7c3aed);border:none;color:white;">
                <h4 style="color:rgba(255,255,255,0.6);">Clinical Evidence Summary</h4>
                <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;">{clin.get('drug_name','')}</div>
                <p style="opacity:0.85;margin-top:0.5rem;font-size:0.9rem;">{clin.get('evidence_overview','')}</p>
            </div>""", unsafe_allow_html=True)

            st.markdown("**Key Clinical Trials**")
            for trial in clin.get("key_trials", []):
                st.markdown(f"""
                <div class="trial-card">
                    <h5>{trial.get('trial_name','')}</h5>
                    <div class="meta">{trial.get('design','')} · n = {trial.get('n_patients','')}</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;font-size:0.85rem;">
                        <div>
                            <div style="color:#94a3b8;font-size:0.73rem;margin-bottom:0.2rem;">PRIMARY ENDPOINT</div>
                            <div style="color:#374151;">{trial.get('primary_endpoint','')}</div>
                        </div>
                        <div>
                            <div style="color:#94a3b8;font-size:0.73rem;margin-bottom:0.2rem;">KEY RESULT</div>
                            <div class="trial-result">{trial.get('key_result','')}</div>
                        </div>
                    </div>
                    <div style="margin-top:0.5rem;font-size:0.75rem;color:#94a3b8;font-style:italic;">{trial.get('reference','')}</div>
                </div>""", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                eff = "".join(f'<li>{h}</li>' for h in clin.get("efficacy_highlights",[]))
                st.markdown(f"""<div class="card card-accent">
                    <h4>✓ Efficacy Highlights</h4>
                    <ul>{eff}</ul>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="card">
                    <h4>🛡️ Safety Profile</h4>
                    <p>{clin.get('safety_profile','')}</p>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="card card-info">
                <h4>🏥 Place in Therapy</h4>
                <p>{clin.get('place_in_therapy','')}</p>
            </div>""", unsafe_allow_html=True)

            # PubMed links
            papers = raw_data.get("pubmed", [])
            if papers:
                st.markdown("**PubMed References Used**")
                for p in papers:
                    st.markdown(
                        f"📄 [{p['title'][:90]}…]({p['url']})  \n"
                        f"<span style='font-size:0.75rem;color:#94a3b8;'>{p['authors']} · {p['journal']} · {p['year']}</span>",
                        unsafe_allow_html=True
                    )

    # ════════════════════════════════════════════════════════════════
    # TAB 5 — RAW DATA
    # ════════════════════════════════════════════════════════════════
    with tab5:
        st.caption("Raw API responses — for verification and debugging")
        with st.expander("🏛️ FDA Label (OpenFDA)", expanded=False):
            st.json(raw_data.get("fda_label", {}))
        with st.expander("💊 DailyMed", expanded=False):
            st.json(raw_data.get("dailymed", {}))
        with st.expander("🔬 PubMed Papers", expanded=False):
            st.json(raw_data.get("pubmed", []))
        with st.expander("⚠️ Adverse Events (FAERS)", expanded=False):
            st.json(raw_data.get("adverse_events", []))

elif not trigger:
    # Landing state
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;color:#94a3b8;">
        <div style="font-size:3rem;margin-bottom:1rem;">💊</div>
        <div style="font-size:1.1rem;color:#64748b;margin-bottom:0.5rem;">Enter a drug name above and click Generate</div>
        <div style="font-size:0.85rem;">Or pick one from the sidebar examples</div>
    </div>
    """, unsafe_allow_html=True)
