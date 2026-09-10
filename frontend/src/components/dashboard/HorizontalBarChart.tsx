interface BarItem { risk_type: string; percentage: number; color: string }
interface Props { data: BarItem[]; title: string }

export default function HorizontalBarChart({ data, title }: Props) {
  return (
    <div className="card">
      <h3 className="font-bold text-slate-800 mb-4 text-sm">{title}</h3>
      <div className="space-y-3">
        {data.map((item, i) => (
          <div key={i}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-slate-600 font-medium">{item.risk_type}</span>
              <span className="text-slate-800 font-bold">{item.percentage}%</span>
            </div>
            <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full rounded-full transition-all duration-700" style={{ width: `${item.percentage}%`, backgroundColor: item.color }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}