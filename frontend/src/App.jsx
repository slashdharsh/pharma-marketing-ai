import { useState } from "react"
import DrugSearch from "./components/DrugSearch"
import HCPDetailAid from "./components/HCPDetailAid"
import PatientLeaflet from "./components/PatientLeaflet"
import PackageInsert from "./components/PackageInsert"
import ClinicalEvidence from "./components/ClinicalEvidence"
import RawDataPanel from "./components/RawDataPanel"
import { Pill, FlaskConical, FileText, Users, BookOpen, Database } from "lucide-react"

const TABS = [
  { id: "hcp_detail_aid",   label: "HCP Detail Aid",        icon: Users },
  { id: "patient_leaflet",  label: "Patient Leaflet",        icon: Pill },
  { id: "package_insert",   label: "Package Insert",         icon: FileText },
  { id: "clinical_evidence",label: "Clinical Evidence",      icon: BookOpen },
  { id: "raw",              label: "Raw Data",               icon: Database },
]

export default function App() {
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)
  const [activeTab, setActiveTab] = useState("hcp_detail_aid")

  async function handleSearch(drugName, contentType) {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await fetch("/api/drug/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ drug_name: drugName, content_type: "all" }),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || "Something went wrong")
      }
      const data = await res.json()
      setResult(data)
      setActiveTab("hcp_detail_aid")
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-3">
          <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-pharma-600">
            <FlaskConical size={18} className="text-white" />
          </div>
          <div>
            <h1 className="font-display text-xl text-pharma-900 leading-none">Pharma Marketing AI</h1>
            <p className="text-xs text-slate-400 mt-0.5">Powered by OpenFDA · DailyMed · PubMed · Groq</p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Search */}
        <DrugSearch onSearch={handleSearch} loading={loading} />

        {/* Error */}
        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm fade-up">
            ⚠️ {error}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="mt-12 flex flex-col items-center gap-4 fade-up">
            <div className="w-12 h-12 rounded-full border-4 border-pharma-200 border-t-pharma-600 spinning" />
            <p className="text-slate-500 text-sm">Fetching from FDA · DailyMed · PubMed…</p>
            <p className="text-slate-400 text-xs">Generating content with Groq AI…</p>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="mt-8 fade-up">
            {/* Drug name banner */}
            <div className="mb-6 p-5 bg-pharma-600 rounded-2xl text-white flex items-center justify-between">
              <div>
                <p className="text-pharma-200 text-xs uppercase tracking-widest mb-1">Results for</p>
                <h2 className="font-display text-3xl capitalize">{result.drug_name}</h2>
                {result.raw_data?.fda_label?.brand_name && (
                  <p className="text-pharma-200 text-sm mt-1">
                    {result.raw_data.fda_label.brand_name} · {result.raw_data.fda_label.generic_name}
                  </p>
                )}
              </div>
              <div className="text-right text-pharma-200 text-xs space-y-1">
                <div>✓ FDA Label</div>
                <div>✓ DailyMed</div>
                <div>✓ PubMed ({result.raw_data?.pubmed?.length || 0} papers)</div>
              </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-1 mb-6 bg-white p-1 rounded-xl border border-slate-200 shadow-sm overflow-x-auto">
              {TABS.map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  onClick={() => setActiveTab(id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all
                    ${activeTab === id
                      ? "bg-pharma-600 text-white shadow"
                      : "text-slate-500 hover:text-pharma-700 hover:bg-pharma-50"
                    }`}
                >
                  <Icon size={14} />
                  {label}
                </button>
              ))}
            </div>

            {/* Tab content */}
            <div className="fade-up">
              {activeTab === "hcp_detail_aid"    && <HCPDetailAid data={result.content?.hcp_detail_aid} />}
              {activeTab === "patient_leaflet"   && <PatientLeaflet data={result.content?.patient_leaflet} />}
              {activeTab === "package_insert"    && <PackageInsert data={result.content?.package_insert} />}
              {activeTab === "clinical_evidence" && <ClinicalEvidence data={result.content?.clinical_evidence} />}
              {activeTab === "raw"               && <RawDataPanel data={result.raw_data} />}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
