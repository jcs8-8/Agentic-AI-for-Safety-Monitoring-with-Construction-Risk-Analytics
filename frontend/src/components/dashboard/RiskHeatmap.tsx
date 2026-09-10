import { useState } from 'react'

interface HeatmapCell { probability: number; impact: number; count: number; risk_level: string }
interface RiskHeatmapProps {
  data: { inherent: HeatmapCell[]; residual: HeatmapCell[] }
}

const PROB_LABELS = ['', 'Rare', 'Unlikely', 'Possible', 'Likely', 'Almost Certain']
const IMPACT_LABELS = ['', 'Negligible', 'Minor', 'Moderate', 'Major', 'Catastrophic']
const RISK_COLORS: Record<string, string> = {
  'Low': '#22c55e', 'Low-Medium': '#86efac', 'Medium': '#facc15',
  'Medium-High': '#fb923c', 'High': '#f87171', 'Critical': '#dc2626', 'Extreme': '#7f1d1d'
}

export default function RiskHeatmap({ data }: RiskHeatmapProps) {
  const [tab, setTab] = useState<'inherent' | 'residual'>('inherent')
  const cells = tab === 'inherent' ? data.inherent : data.residual
  const matrix: Record<string, HeatmapCell> = {}
  cells.forEach(c => { matrix[`${c.probability}-${c.impact}`] = c })
  const rowTotals: Record<number, number> = {}
  const colTotals: Record<number, number> = {}
  cells.forEach(c => {
    rowTotals[c.probability] = (rowTotals[c.probability] || 0) + c.count
    colTotals[c.impact] = (colTotals[c.impact] || 0) + c.count
  })

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-slate-800 text-sm">Risk Heat Map — Probability × Impact Matrix</h3>
        <div className="flex bg-slate-100 rounded-lg p-1">
          <button onClick={() => setTab('inherent')} className={`px-3 py-1 text-xs rounded-md transition ${tab === 'inherent' ? 'bg-white shadow-sm font-medium' : 'text-slate-500'}`}>Inherent Risk</button>
          <button onClick={() => setTab('residual')} className={`px-3 py-1 text-xs rounded-md transition ${tab === 'residual' ? 'bg-white shadow-sm font-medium' : 'text-slate-500'}`}>Residual Risk</button>
        </div>
      </div>
      <div className="flex gap-4">
        <div className="flex-1 overflow-x-auto">
          <div className="grid grid-cols-6 gap-0.5 min-w-[400px]">
            <div></div>
            {IMPACT_LABELS.slice(1).map((l, i) => (
              <div key={i} className="text-[10px] text-slate-500 text-center font-medium pb-1">{i+1}<br/><span className="text-slate-400">{l.slice(0,6)}</span></div>
            ))}
            {[5,4,3,2,1].map(prob => (
              <>
                <div key={`l${prob}`} className="text-[10px] text-slate-500 font-medium flex items-center pr-1">{prob} {PROB_LABELS[prob].slice(0,8)}</div>
                {[1,2,3,4,5].map(imp => {
                  const cell = matrix[`${prob}-${imp}`]
                  const count = cell?.count || 0
                  const level = cell?.risk_level || 'Low'
                  return (
                    <div key={`${prob}-${imp}`} className="aspect-square rounded-sm flex items-center justify-center text-xs font-bold"
                      style={{ backgroundColor: count > 0 ? RISK_COLORS[level] : '#f1f5f9', color: count > 0 ? 'white' : '#cbd5e1' }}>
                      {count > 0 ? count : prob * imp}
                    </div>
                  )
                })}
              </>
            ))}
            <div className="text-[10px] text-slate-400 text-center pt-1">Total</div>
            {[1,2,3,4,5].map(imp => (
              <div key={`ct${imp}`} className="text-xs font-bold text-slate-600 text-center pt-1">{colTotals[imp] || 0}</div>
            ))}
          </div>
        </div>
        <div className="w-32 flex-shrink-0">
          <p className="text-[10px] font-bold text-slate-700 mb-2">LEGEND</p>
          {Object.entries(RISK_COLORS).map(([level, color]) => (
            <div key={level} className="flex items-center gap-1.5 mb-1">
              <div className="w-3 h-3 rounded" style={{ backgroundColor: color }}></div>
              <span className="text-[10px] text-slate-600">{level}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}