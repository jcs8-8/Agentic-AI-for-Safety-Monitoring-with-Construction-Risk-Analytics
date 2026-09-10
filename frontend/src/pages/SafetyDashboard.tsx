import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { CheckCircle2, Shield, BarChart2 } from 'lucide-react'
import { api } from '@/lib/api'
import KpiCard from '@/components/dashboard/KpiCard'
import HorizontalBarChart from '@/components/dashboard/HorizontalBarChart'
import CircularGauge from '@/components/dashboard/CircularGauge'
import { useSocket } from '@/hooks/useSocket'

const iconMap: Record<string, any> = { 'check-circle': CheckCircle2, 'alert-triangle': Shield, 'users': Shield, 'shield': Shield }

export default function SafetyDashboard() {
  const { projectId } = useParams()
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const id = projectId || 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'

  useEffect(() => {
    api.get(`/projects/${id}/dashboard/safety`).then(r => { setData(r.data.data); setLoading(false) })
  }, [projectId])

  useSocket(id, () => {
    api.get(`/projects/${id}/dashboard/safety`).then(r => setData(r.data.data))
  })

  if (loading) return <div className="flex items-center justify-center h-full text-slate-500">Loading...</div>
  if (!data) return <div className="text-center text-slate-500">No data available</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Safety Intelligence Dashboard</h2>
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
              <CheckCircle2 className="w-5 h-5 text-accent-orange" /> Safety Intelligence Features
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
          <div className="card flex items-center justify-center py-8">
            <CircularGauge value={data.ppe_compliance_rate} label="PPE Compliance" />
          </div>
        </div>
        <div className="space-y-6">
          <div>
            <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
              <BarChart2 className="w-5 h-5 text-accent-orange" /> Key Performance Indicators
            </h3>
            <div className="grid grid-cols-2 gap-4">
              {data.kpis.map((kpi: any, i: number) => (
                <KpiCard key={i} label={kpi.label} value={kpi.value} icon={iconMap[kpi.icon] || Shield} color={kpi.color} />
              ))}
            </div>
          </div>
          <HorizontalBarChart data={data.ppe_by_type.map((p: any) => ({ risk_type: p.type, percentage: p.rate, color: p.color }))} title="Safety Compliance by PPE Type" />
          <div className="card">
            <h3 className="font-bold text-slate-800 mb-4 text-sm">Recent Incidents</h3>
            <div className="space-y-2">
              {data.recent_incidents.map((inc: any, i: number) => (
                <div key={i} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-slate-700">{inc.type}</p>
                    <p className="text-xs text-slate-500">Severity: {inc.severity}</p>
                  </div>
                  <span className="text-xs text-slate-400">{new Date(inc.date).toLocaleDateString()}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}