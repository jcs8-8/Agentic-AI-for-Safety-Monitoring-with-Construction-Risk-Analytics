interface Props {
  categories: Array<{ category: string; score: number; color: string }>
}

export default function ComplianceProgress({ categories }: Props) {
  return (
    <div className="card">
      <h3 className="font-bold text-slate-800 mb-4 text-sm">Compliance Status by Category</h3>
      <div className="space-y-3">
        {categories.map((c, i) => (
          <div key={i}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-slate-600">{c.category}</span>
              <span className="text-slate-800 font-bold">{c.score}%</span>
            </div>
            <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full rounded-full transition-all duration-700" style={{ width: `${c.score}%`, backgroundColor: c.color }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}