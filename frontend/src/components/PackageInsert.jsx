import Card from "./ui/Card"
import BadgeList from "./ui/BadgeList"

export default function PackageInsert({ data }) {
  if (!data) return <p className="text-slate-400 text-center py-12 text-sm">No package insert generated yet.</p>
  if (data.parse_error) return <pre className="whitespace-pre-wrap text-xs bg-slate-100 p-4 rounded-xl">{data.raw_text}</pre>

  return (
    <div className="space-y-5">
      <div className="p-7 rounded-2xl bg-slate-800 text-white">
        <p className="text-slate-400 text-xs uppercase tracking-widest mb-1">Package Insert / Prescribing Information</p>
        <h2 className="font-display text-3xl">{data.brand_name}</h2>
        <p className="text-slate-300 text-lg">({data.generic_name}) · {data.drug_class}</p>
      </div>

      <Card title="Indications and Usage">
        <p className="text-slate-600 text-sm leading-relaxed">{data.indications_and_usage}</p>
      </Card>

      <Card title="Dosage and Administration">
        <p className="text-slate-600 text-sm leading-relaxed whitespace-pre-line">{data.dosage_and_administration}</p>
      </Card>

      <div className="grid md:grid-cols-2 gap-5">
        <Card title="Contraindications" className="bg-red-50 border-red-200">
          <BadgeList items={data.contraindications} color="red" />
        </Card>
        <Card title="Warnings & Precautions" className="bg-amber-50 border-amber-200">
          <BadgeList items={data.warnings_and_precautions} color="amber" />
        </Card>
      </div>

      <Card title="Adverse Reactions">
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <p className="text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wide">Common</p>
            <BadgeList items={data.adverse_reactions?.common} color="blue" />
          </div>
          <div>
            <p className="text-xs font-semibold text-red-500 mb-2 uppercase tracking-wide">Serious</p>
            <BadgeList items={data.adverse_reactions?.serious} color="red" />
          </div>
        </div>
      </Card>

      <Card title="Drug Interactions">
        <BadgeList items={data.drug_interactions} color="purple" />
      </Card>

      <Card title="Use in Specific Populations">
        <div className="grid md:grid-cols-2 gap-3 text-sm text-slate-600">
          {Object.entries(data.use_in_specific_populations || {}).map(([k, v]) => (
            <div key={k} className="p-3 bg-slate-50 rounded-lg">
              <p className="font-semibold text-slate-700 capitalize mb-1">{k.replace(/_/g, " ")}</p>
              <p>{v}</p>
            </div>
          ))}
        </div>
      </Card>

      <div className="grid md:grid-cols-2 gap-5">
        <Card title="Mechanism of Action">
          <p className="text-slate-600 text-sm leading-relaxed">{data.mechanism_of_action}</p>
        </Card>
        <Card title="Pharmacokinetics">
          <p className="text-slate-600 text-sm leading-relaxed">{data.pharmacokinetics}</p>
        </Card>
      </div>

      <Card title="Clinical Trials">
        <p className="text-slate-600 text-sm leading-relaxed">{data.clinical_trials}</p>
      </Card>

      <Card title="How Supplied">
        <p className="text-slate-600 text-sm">{data.how_supplied}</p>
      </Card>
    </div>
  )
}
