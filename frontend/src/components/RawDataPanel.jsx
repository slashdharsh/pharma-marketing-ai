import { useState } from "react"

const SECTIONS = [
  { key: "fda_label",     label: "FDA Label" },
  { key: "dailymed",      label: "DailyMed" },
  { key: "pubmed",        label: "PubMed Papers" },
  { key: "adverse_events",label: "Adverse Events (FAERS)" },
]

export default function RawDataPanel({ data }) {
  const [open, setOpen] = useState("fda_label")
  if (!data) return null

  return (
    <div className="space-y-3">
      <p className="text-xs text-slate-400">Raw API responses — for debugging & verification</p>
      {SECTIONS.map(({ key, label }) => (
        <div key={key} className="bg-white border border-slate-200 rounded-xl overflow-hidden">
          <button
            onClick={() => setOpen(open === key ? null : key)}
            className="w-full flex items-center justify-between px-5 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50 transition"
          >
            {label}
            <span className="text-slate-300">{open === key ? "▲" : "▼"}</span>
          </button>
          {open === key && (
            <pre className="px-5 py-4 text-xs overflow-auto bg-slate-50 border-t border-slate-100 text-slate-600 max-h-96">
              {JSON.stringify(data[key], null, 2)}
            </pre>
          )}
        </div>
      ))}
    </div>
  )
}
