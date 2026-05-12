import { ShieldCheck, Target, Zap, Users } from "lucide-react"
import Card from "./ui/Card"
import BadgeList from "./ui/BadgeList"

export default function HCPDetailAid({ data }) {
  if (!data) return <EmptyState />
  if (data.parse_error) return <RawText text={data.raw_text} />

  return (
    <div className="space-y-5">
      {/* Hero */}
      <div className="p-7 rounded-2xl bg-gradient-to-r from-pharma-700 to-pharma-500 text-white">
        <div className="flex justify-between items-start gap-4 flex-wrap">
          <div>
            <p className="text-pharma-200 text-xs uppercase tracking-widest mb-1">{data.drug_class}</p>
            <h2 className="font-display text-4xl">{data.brand_name || data.generic_name}</h2>
            {data.brand_name && <p className="text-pharma-200 text-lg mt-1">({data.generic_name})</p>}
            <p className="text-pharma-100 mt-3 text-sm max-w-xl">{data.tagline}</p>
          </div>
          <div className="text-right text-pharma-200 text-xs">HCP Detail Aid</div>
        </div>
        <div className="mt-6 p-4 bg-white/10 rounded-xl">
          <p className="text-white font-semibold text-lg font-display italic">"{data.headline}"</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Indication */}
        <Card title="Indication" icon={<Target size={16} />}>
          <p className="text-slate-600 text-sm leading-relaxed">{data.indication}</p>
        </Card>

        {/* MOA */}
        <Card title="Mechanism of Action" icon={<Zap size={16} />}>
          <p className="text-slate-600 text-sm leading-relaxed">{data.mechanism_of_action}</p>
        </Card>
      </div>

      {/* Efficacy */}
      <Card title="Key Efficacy Points" icon={<ShieldCheck size={16} />} accent>
        <ul className="space-y-2">
          {(data.key_efficacy_points || []).map((pt, i) => (
            <li key={i} className="flex items-start gap-3 text-sm text-slate-700">
              <span className="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full bg-accent/20 text-accent text-xs flex items-center justify-center font-bold">{i+1}</span>
              {pt}
            </li>
          ))}
        </ul>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Dosing */}
        <Card title="Dosing Summary">
          <p className="text-slate-600 text-sm leading-relaxed whitespace-pre-line">{data.dosing_summary}</p>
        </Card>

        {/* Patient Selection */}
        <Card title="Patient Selection" icon={<Users size={16} />}>
          <p className="text-slate-600 text-sm leading-relaxed">{data.patient_selection}</p>
        </Card>
      </div>

      {/* Safety */}
      <Card title="Safety Highlights" className="border-amber-200 bg-amber-50">
        <BadgeList items={data.safety_highlights} color="amber" />
      </Card>

      {/* References */}
      {data.references?.length > 0 && (
        <div className="text-xs text-slate-400 space-y-1 pt-2 border-t border-slate-100">
          <p className="font-medium text-slate-500 mb-2">References</p>
          {data.references.map((r, i) => <p key={i}>{i+1}. {r}</p>)}
        </div>
      )}
    </div>
  )
}

function EmptyState() {
  return <p className="text-slate-400 text-sm text-center py-12">No HCP detail aid generated yet.</p>
}
function RawText({ text }) {
  return <pre className="whitespace-pre-wrap text-xs bg-slate-100 p-4 rounded-xl">{text}</pre>
}
