# Pharma Marketing AI — Streamlit App

## Run Locally

```bash
cd streamlit_app

# 1. Install deps
pip install -r requirements.txt

# 2. Run
streamlit run app.py
```

Open http://localhost:8501 — enter your Groq key in the sidebar and search any drug.

---

## Deploy to Streamlit Cloud (Free Hosting)

1. Push your project to a **GitHub repo**
2. Go to **https://share.streamlit.io**
3. Click **"New app"**
4. Set:
   - **Repo**: your GitHub repo
   - **Branch**: main
   - **Main file path**: `streamlit_app/app.py`
5. Click **"Advanced settings" → Secrets** and paste:
   ```
   GROQ_API_KEY = "gsk_your_key_here"
   ```
6. Click **Deploy** — live in ~2 minutes ✓

---

## Project Structure

```
streamlit_app/
├── app.py                    ← Main Streamlit app (all UI)
├── drug_fetcher.py           ← OpenFDA, DailyMed, PubMed agents
├── content_generator.py      ← Groq AI content generation
├── requirements.txt          ← Python dependencies
└── .streamlit/
    ├── config.toml           ← Theme & server config
    └── secrets.toml.example  ← Secrets template
```
