import Card from "./ui/Card"
import BadgeList from "./ui/BadgeList"
import { Heart, AlertTriangle, Info } from "lucide-react"

export default function PatientLeaflet({ data }) {
  if (!data) return <p className="text-slate-400 text-center py-12 text-sm">No patient leaflet generated yet.</p>
  if (data.parse_error) return <pre className="whitespace-pre-wrap text-xs bg-slate-100 p-4 rounded-xl">{data.raw_text}</pre>

  return (
    <div className="space-y-5">
      <div className="p-7 rounded-2xl bg-gradient-to-r from-accent to-teal-500 text-white">
        <p className="text-white/70 text-xs uppercase tracking-widest mb-1">Patient Information</p>
        <h2 className="font-display text-3xl">{data.title}</h2>
      </div>

      <div className="grid md:grid-cols-2 gap-5">
        <Card title="What is this medicine?" icon={<Info size={16} />}>
          <p className="text-slate-600 text-sm leading-relaxed">{data.what_is_it}</p>
        </Card>
        <Card title="How does it work?" icon={<Heart size={16} />}>
          <p className="text-slate-600 text-sm leading-relaxed">{data.how_it_works}</p>
        </Card>
      </div>

      <Card title="How to take it">
        <p className="text-slate-600 text-sm leading-relaxed whitespace-pre-line">{data.how_to_take}</p>
      </Card>

      <Card title="What you might feel">
        <p className="text-slate-600 text-sm leading-relaxed">{data.what_to_expect}</p>
      </Card>

      <div className="grid md:grid-cols-2 gap-5">
        <Card title="Possible Side Effects" className="bg-orange-50 border-orange-200">
          <BadgeList items={data.side_effects} color="orange" />
        </Card>
        <Card title="When to call your doctor" icon={<AlertTriangle size={16} />} className="bg-red-50 border-red-200">
          <BadgeList items={data.when_to_call_doctor} color="red" />
        </Card>
      </div>

      <div className="grid md:grid-cols-2 gap-5">
        <Card title="Storage"><p className="text-slate-600 text-sm">{data.storage}</p></Card>
        <Card title="Important Reminders"><BadgeList items={data.important_reminders} color="blue" /></Card>
      </div>
    </div>
  )
}
