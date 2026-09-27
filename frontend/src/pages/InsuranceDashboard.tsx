import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '@/lib/api'
import { useSocket } from '@/hooks/useSocket'

interface ClaimAnalysis { type: string; count: number; avg_risk: number }
interface InsuranceData {
  insurance_risk_score: string
  average_risk_score: number
  total_exposure: number
  open_exposure: number
  cost_savings_estimate: number
  open_cases: number
  claim_analysis: ClaimAnalysis[]
}

export default function InsuranceDashboard() {
  const { projectId } = useParams()
  const [data, setData] = useState<InsuranceData | null>(null)
  const [loading, setLoading] = useState(true)
  const id = projectId || 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'

  useEffect(() => {
    api.get(`/projects/${id}/insurance/dashboard`).then(r => { setData(r.data.data); setLoading(false) })
  }, [projectId])

  useSocket(id, () => {
    api.get(`/projects/${id}/insurance/dashboard`).then(r => setData(r.data.data))
  })

  if (loading) return <div className="flex items-center justify-center h-full text-slate-500">Loading...</div>
  if (!data) return <div className="text-center text-slate-500">No data available</div>

  return (
    <div>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Insurance Dashboard</h2>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="card"><p className="kpi-label">Risk Score</p><p className="kpi-value text-status-warning">{data.insurance_risk_score}</p></div>
        <div className="card"><p className="kpi-label">Total Exposure</p><p className="kpi-value">${(data.total_exposure / 1000000).toFixed(1)}M</p></div>
        <div className="card"><p className="kpi-label">Open Cases</p><p className="kpi-value text-status-danger">{data.open_cases}</p></div>
        <div className="card"><p className="kpi-label">Cost Savings Estimate</p><p className="kpi-value text-status-success">${(data.cost_savings_estimate / 1000).toFixed(0)}K</p></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="card"><p className="kpi-label">Open Exposure</p><p className="kpi-value">${(data.open_exposure / 1000000).toFixed(1)}M</p></div>
        <div className="card"><p className="kpi-label">Average Risk Score</p><p className="kpi-value">{data.average_risk_score}/100</p></div>
      </div>
      <div className="card">
        <h3 className="font-bold text-slate-800 mb-4">Claim Risk Analysis</h3>
        <div className="space-y-3">
          {data.claim_analysis.map((c, i) => (
            <div key={i} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
              <div>
                <p className="text-sm font-medium text-slate-700">{c.type}</p>
                <p className="text-xs text-slate-500">{c.count} cases</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-bold text-slate-800">{c.avg_risk}/100</p>
                <p className="text-xs text-slate-500">Avg Risk</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}