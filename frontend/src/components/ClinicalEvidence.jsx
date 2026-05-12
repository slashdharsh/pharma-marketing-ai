import Card from "./ui/Card"
import { ExternalLink } from "lucide-react"

export default function ClinicalEvidence({ data }) {
  if (!data) return <p className="text-slate-400 text-center py-12 text-sm">No clinical evidence generated yet.</p>
  if (data.parse_error) return <pre className="whitespace-pre-wrap text-xs bg-slate-100 p-4 rounded-xl">{data.raw_text}</pre>

  return (
    <div className="space-y-5">
      <div className="p-7 rounded-2xl bg-gradient-to-r from-violet-700 to-purple-500 text-white">
        <p className="text-white/60 text-xs uppercase tracking-widest mb-1">Clinical Evidence Summary</p>
        <h2 className="font-display text-3xl">{data.drug_name}</h2>
        <p className="text-white/80 mt-3 text-sm max-w-2xl">{data.evidence_overview}</p>
      </div>

      <Card title="Key Clinical Trials">
        <div className="space-y-4">
          {(data.key_trials || []).map((trial, i) => (
            <div key={i} className="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div>
                  <p className="font-semibold text-slate-800">{trial.trial_name}</p>
                  <p className="text-xs text-slate-400 mt-0.5">{trial.design} · n={trial.n_patients}</p>
                </div>
                <span className="text-xs bg-violet-100 text-violet-700 px-2 py-1 rounded-full font-medium">
                  {trial.design}
                </span>
              </div>
              <div className="mt-3 grid md:grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-xs text-slate-400 mb-1">Primary Endpoint</p>
                  <p className="text-slate-700">{trial.primary_endpoint}</p>
                </div>
                <div>
                  <p className="text-xs text-slate-400 mb-1">Key Result</p>
                  <p className="text-slate-700 font-medium text-accent-dark">{trial.key_result}</p>
                </div>
              </div>
              {trial.reference && (
                <p className="mt-2 text-xs text-slate-400 italic">{trial.reference}</p>
              )}
            </div>
          ))}
        </div>
      </Card>

      <div className="grid md:grid-cols-2 gap-5">
        <Card title="Efficacy Highlights">
          <ul className="space-y-2">
            {(data.efficacy_highlights || []).map((h, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-slate-700">
                <span className="text-accent mt-0.5">✓</span> {h}
              </li>
            ))}
          </ul>
        </Card>
        <Card title="Safety Profile">
          <p className="text-slate-600 text-sm leading-relaxed">{data.safety_profile}</p>
        </Card>
      </div>

      <Card title="Place in Therapy">
        <p className="text-slate-600 text-sm leading-relaxed">{data.place_in_therapy}</p>
      </Card>
    </div>
  )
}
