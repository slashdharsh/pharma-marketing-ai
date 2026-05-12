import { useState } from "react"
import { Search, Loader2 } from "lucide-react"

const EXAMPLE_DRUGS = ["Metformin", "Atorvastatin", "Lisinopril", "Omeprazole", "Sertraline", "Amoxicillin"]

export default function DrugSearch({ onSearch, loading }) {
  const [drug, setDrug] = useState("")

  function handleSubmit(e) {
    e.preventDefault()
    if (drug.trim()) onSearch(drug.trim())
  }

  return (
    <div className="max-w-2xl mx-auto text-center">
      <h2 className="font-display text-4xl text-pharma-900 mb-2">Drug Intelligence Search</h2>
      <p className="text-slate-500 mb-8 text-sm">
        Enter any drug name to generate HCP aids, patient leaflets, package inserts & clinical evidence summaries.
      </p>

      <form onSubmit={handleSubmit} className="relative">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              value={drug}
              onChange={e => setDrug(e.target.value)}
              placeholder="e.g. Metformin, Atorvastatin, Lisinopril…"
              disabled={loading}
              className="w-full pl-11 pr-4 py-3.5 rounded-xl border border-slate-300 bg-white shadow-sm text-sm
                         focus:outline-none focus:ring-2 focus:ring-pharma-500 focus:border-pharma-500
                         disabled:opacity-50 transition"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !drug.trim()}
            className="px-6 py-3.5 bg-pharma-600 hover:bg-pharma-700 disabled:opacity-50
                       text-white text-sm font-medium rounded-xl shadow transition-colors flex items-center gap-2"
          >
            {loading ? <Loader2 size={16} className="spinning" /> : <Search size={16} />}
            {loading ? "Generating…" : "Generate"}
          </button>
        </div>
      </form>

      <div className="mt-4 flex flex-wrap justify-center gap-2">
        <span className="text-xs text-slate-400 self-center">Try:</span>
        {EXAMPLE_DRUGS.map(d => (
          <button
            key={d}
            onClick={() => { setDrug(d); onSearch(d) }}
            disabled={loading}
            className="text-xs px-3 py-1 rounded-full bg-white border border-slate-200
                       text-slate-600 hover:border-pharma-400 hover:text-pharma-600 transition disabled:opacity-40"
          >
            {d}
          </button>
        ))}
      </div>
    </div>
  )
}
