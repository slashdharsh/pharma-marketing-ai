export default function Card({ title, icon, children, className = "", accent = false }) {
  return (
    <div className={`bg-white rounded-2xl border p-5 shadow-sm ${accent ? "border-accent/30" : "border-slate-200"} ${className}`}>
      {title && (
        <div className="flex items-center gap-2 mb-4">
          {icon && <span className="text-pharma-500">{icon}</span>}
          <h3 className="text-sm font-semibold text-slate-700 uppercase tracking-wide">{title}</h3>
        </div>
      )}
      {children}
    </div>
  )
}
