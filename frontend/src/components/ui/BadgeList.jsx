const COLOR_MAP = {
  amber:  "bg-amber-100 text-amber-800",
  red:    "bg-red-100 text-red-700",
  blue:   "bg-blue-100 text-blue-700",
  green:  "bg-green-100 text-green-700",
  orange: "bg-orange-100 text-orange-700",
  purple: "bg-purple-100 text-purple-700",
}

export default function BadgeList({ items = [], color = "blue" }) {
  const cls = COLOR_MAP[color] || COLOR_MAP.blue
  return (
    <div className="flex flex-wrap gap-2">
      {(items || []).map((item, i) => (
        <span key={i} className={`text-xs px-2.5 py-1 rounded-full font-medium ${cls}`}>
          {item}
        </span>
      ))}
    </div>
  )
}
