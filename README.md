# Pharma Marketing AI — Phase 1 (Local)

AI-powered pharma content generator: type a drug name, get HCP detail aids,
patient leaflets, package inserts & clinical evidence summaries — sourced from
FDA, DailyMed, and PubMed in real time.

## Tech Stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Backend      | Python 3.11+ · FastAPI · Uvicorn    |
| AI Brain     | Groq API (free) — Llama 3.3 70B     |
| Data Sources | OpenFDA · DailyMed · PubMed (free, no key) |
| Frontend     | React 18 · Vite · Tailwind CSS      |

---

## Setup (One-Time)

### 1. Clone / open the project in VS Code
```
cd pharma-marketing-ai
```

### 2. Get your FREE Groq API Key
- Go to https://console.groq.com
- Sign up → API Keys → Create Key
- Copy it

### 3. Create your .env file
```bash
cp .env.example .env
# Now edit .env and paste your Groq key:
# GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

### 4. Backend setup
```bash
cd backend
python -m venv venv

# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

### 5. Frontend setup
```bash
cd ../frontend
npm install
```

---

## Running the App

You need **two terminals** open in VS Code:

### Terminal 1 — Backend
```bash
cd backend
source venv/bin/activate   # (or venv\Scripts\activate on Windows)
uvicorn main:app --reload --port 8000
```
→ API running at http://localhost:8000
→ API docs at http://localhost:8000/docs

### Terminal 2 — Frontend
```bash
cd frontend
npm run dev
```
→ App running at http://localhost:5173

---

## API Endpoints

| Method | Endpoint                | Description                        |
|--------|-------------------------|------------------------------------|
| GET    | /health                 | Health check                       |
| POST   | /api/drug/generate      | Full generation (data + AI content)|
| POST   | /api/drug/raw           | Raw API data only (no AI)          |
| GET    | /api/drug/search/{name} | Quick drug lookup                  |

### Example cURL test:
```bash
curl -X POST http://localhost:8000/api/drug/generate \
  -H "Content-Type: application/json" \
  -d '{"drug_name": "metformin", "content_type": "all"}'
```

---

## Project Structure
```
pharma-marketing-ai/
├── backend/
│   ├── main.py              # FastAPI app + all routes
│   ├── drug_fetcher.py      # OpenFDA, DailyMed, PubMed agents
│   ├── content_generator.py # Groq AI content generation
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
│           ├── DrugSearch.jsx
│           ├── HCPDetailAid.jsx
│           ├── PatientLeaflet.jsx
│           ├── PackageInsert.jsx
│           ├── ClinicalEvidence.jsx
│           ├── RawDataPanel.jsx
│           └── ui/
│               ├── Card.jsx
│               └── BadgeList.jsx
├── .env.example
└── README.md
```

---

## Phase 2 (Next)
- MOA diagrams (SVG)
- Efficacy bar charts
- PDF export
- Brand color customization

## Phase 3 (Streamlit hosting)
- Everything above wrapped in Streamlit for demo/sharing
