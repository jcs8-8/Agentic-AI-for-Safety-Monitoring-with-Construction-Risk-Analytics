import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { CheckCircle2, BarChart2, AlertTriangle, Shield, FileCheck } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { api } from '@/lib/api'
import KpiCard from '@/components/dashboard/KpiCard'
import ComplianceProgress from '@/components/dashboard/ComplianceProgress'
import { useSocket } from '@/hooks/useSocket'

const iconMap: Record<string, LucideIcon> = { 'check-circle': CheckCircle2, 'alert-triangle': AlertTriangle, shield: Shield, 'file-check': FileCheck }

interface ComplianceCategory { category: string; score: number; color: string }
interface ComplianceData {
  project_name: string
  compliance_kpis: Array<{ label: string; value: string; icon: string; color: string }>
  insurance_kpis: Array<{ label: string; value: string; icon: string; color: string }>
  compliance_by_category: ComplianceCategory[]
  applications: { approval_rate: number; processing_time_days: number | null }
  overdue_inspections: number
  documentation_coverage: number
  upcoming_inspections: Array<{ regulation: string; date: string }>
  features: string[]
}

export default function ComplianceDashboard() {
  const { projectId } = useParams()
  const [data, setData] = useState<ComplianceData | null>(null)
  const [loading, setLoading] = useState(true)
  const id = projectId || 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'

  useEffect(() => {
    api.get(`/projects/${id}/dashboard/compliance`).then(r => { setData(r.data.data); setLoading(false) })
  }, [projectId])

  useSocket(id, () => {
    api.get(`/projects/${id}/dashboard/compliance`).then(r => setData(r.data.data))
  })

  if (loading) return <div className="flex items-center justify-center h-full text-slate-500">Loading...</div>
  if (!data) return <div className="text-center text-slate-500">No data available</div>

  const allKpis = [...(data.compliance_kpis || []), ...(data.insurance_kpis || [])]

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Compliance & Insurance Dashboard</h2>
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
              <CheckCircle2 className="w-5 h-5 text-accent-orange" /> Compliance & Insurance Features
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
            <h3 className="font-bold text-slate-800 mb-4 text-sm">Applications Overview</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-slate-50 rounded-lg">
                <p className="text-2xl font-bold text-slate-800">{data.applications.approval_rate}%</p>
                <p className="text-xs text-slate-500">App Approval Rate</p>
              </div>
              <div className="text-center p-4 bg-slate-50 rounded-lg">
                <p className="text-2xl font-bold text-slate-800">{data.documentation_coverage}%</p>
                <p className="text-xs text-slate-500">Documentation Coverage</p>
              </div>
            </div>
          </div>
          <div className="card">
            <h3 className="font-bold text-slate-800 mb-4 text-sm">Inspection Tracking</h3>
            <p className="text-sm text-slate-600 mb-3">{data.overdue_inspections} overdue inspections</p>
            <div className="space-y-2">
              {data.upcoming_inspections.length === 0 ? <p className="text-sm text-slate-500">No upcoming inspections scheduled.</p> : data.upcoming_inspections.map((inspection) => (
                <div key={`${inspection.regulation}-${inspection.date}`} className="flex justify-between text-sm text-slate-600">
                  <span>{inspection.regulation}</span><span>{new Date(inspection.date).toLocaleDateString()}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="space-y-6">
          <div>
            <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
              <BarChart2 className="w-5 h-5 text-accent-orange" /> Key Performance Indicators
            </h3>
            <div className="grid grid-cols-2 gap-4">
              {allKpis.map((kpi, i) => (
                <KpiCard key={i} label={kpi.label} value={kpi.value} icon={iconMap[kpi.icon] || CheckCircle2} color={kpi.color} />
              ))}
            </div>
          </div>
          <ComplianceProgress categories={data.compliance_by_category} />
        </div>
      </div>
    </div>
  )
}