import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { BarChart2, CheckCircle2 } from 'lucide-react'
import { api } from '@/lib/api'
import KpiCard from '@/components/dashboard/KpiCard'
import AgentPerformanceBar from '@/components/dashboard/AgentPerformanceBar'

const iconMap: Record<string, any> = { 'bar-chart-2': BarChart2, 'shield-check': CheckCircle2, 'trending-up': BarChart2, 'dollar-sign': BarChart2 }

export default function ExecutiveDashboard() {
  const { projectId } = useParams()
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const id = projectId || 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
    api.get(`/projects/${id}/dashboard/executive`).then(r => { setData(r.data.data); setLoading(false) })
  }, [projectId])

  if (loading) return <div className="flex items-center justify-center h-full text-slate-500">Loading...</div>
  if (!data) return <div className="text-center text-slate-500">No data available</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Executive Command Center</h2>
          <p className="text-slate-500">{data.project_name}</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 text-green-700 rounded-full text-sm font-medium">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          Live Monitoring
        </div>
      </div>
      <div className="grid grid-cols-2 gap-6">
        <div className="space-y-6">
          <div className="card">
            <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-accent-orange" /> Command Center Features
            </h3>
            <div className="grid grid-cols-2 gap-3">
              {data.features.map((f: string, i: number) => (
                <div key={i} className="flex items-center gap-2 text-sm text-slate-600">
                  <CheckCircle2 className="w-4 h-4 text-status-success flex-shrink-0" />
                  {f}
                </div>
              ))}
            </div>
          </div>
          <div className="card">
            <h3 className="font-bold text-slate-800 mb-4 text-sm">Site Visualization</h3>
            <div className="bg-slate-100 rounded-lg p-8 text-center">
              <p className="text-slate-500">Interactive 3D Site Model</p>
              <p className="text-xs text-slate-400 mt-2">Zone A: Low Risk | Zone B: High Risk | Zone C: Medium Risk</p>
            </div>
          </div>
        </div>
        <div className="space-y-6">
          <div>
            <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
              <BarChart2 className="w-5 h-5 text-accent-orange" /> Key Performance Indicators
            </h3>
            <div className="grid grid-cols-2 gap-4">
              {data.kpis.map((kpi: any, i: number) => (
                <KpiCard key={i} label={kpi.label} value={kpi.value} icon={iconMap[kpi.icon] || BarChart2} color={kpi.color} />
              ))}
            </div>
          </div>
          <AgentPerformanceBar agents={data.agent_performance} />
          <div className="card">
            <h3 className="font-bold text-slate-800 mb-4 text-sm">AI Recommendations</h3>
            <div className="space-y-2">
              {data.recommendations.map((rec: string, i: number) => (
                <div key={i} className="flex items-start gap-2 p-3 bg-blue-50 rounded-lg">
                  <CheckCircle2 className="w-4 h-4 text-accent-blue flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-slate-700">{rec}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}