import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Building2, AlertTriangle, TrendingUp, Shield, ClipboardCheck, Umbrella, BarChart3 } from 'lucide-react'
import { api } from '@/lib/api'

interface Project { project_id: string; project_name: string; location: string; status: string }

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([])
  const [overview, setOverview] = useState<any>(null)

  useEffect(() => {
    api.get('/dashboard/overview').then(r => setOverview(r.data.data))
    api.get('/projects').then(r => setProjects(r.data.data.projects))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Project Dashboard</h2>
      {overview && (
        <div className="grid grid-cols-4 gap-4 mb-8">
          <div className="card"><p className="kpi-label">Total Projects</p><p className="kpi-value">{overview.total_projects}</p></div>
          <div className="card"><p className="kpi-label">Active Projects</p><p className="kpi-value text-status-success">{overview.active_projects}</p></div>
          <div className="card"><p className="kpi-label">Total Risks</p><p className="kpi-value text-status-warning">{overview.total_risks}</p></div>
          <div className="card"><p className="kpi-label">High Risk Projects</p><p className="kpi-value text-status-danger">{overview.high_risk_projects}</p></div>
        </div>
      )}
      <h3 className="text-lg font-bold text-slate-800 mb-4">Projects</h3>
      <div className="grid grid-cols-3 gap-4">
        {projects.map(p => (
          <Link key={p.project_id} to={`/site-risk/${p.project_id}`} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="w-10 h-10 rounded-lg bg-accent-orange/10 flex items-center justify-center">
                <Building2 className="w-5 h-5 text-accent-orange" />
              </div>
              <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full font-medium">{p.status}</span>
            </div>
            <h4 className="font-bold text-slate-800 mt-3">{p.project_name}</h4>
            <p className="text-sm text-slate-500 mt-1">{p.location}</p>
            <div className="flex items-center gap-2 mt-4 text-sm text-accent-orange font-medium">
              <AlertTriangle className="w-4 h-4" />
              View Site Risk Dashboard
              <TrendingUp className="w-4 h-4" />
            </div>
          </Link>
        ))}
      </div>
      <div className="grid grid-cols-4 gap-4 mt-8">
        <Link to="/safety" className="card hover:shadow-md transition text-center">
          <Shield className="w-8 h-8 text-status-success mx-auto mb-2" />
          <p className="font-medium text-slate-700">Safety</p>
        </Link>
        <Link to="/compliance" className="card hover:shadow-md transition text-center">
          <ClipboardCheck className="w-8 h-8 text-accent-blue mx-auto mb-2" />
          <p className="font-medium text-slate-700">Compliance</p>
        </Link>
        <Link to="/insurance" className="card hover:shadow-md transition text-center">
          <Umbrella className="w-8 h-8 text-status-warning mx-auto mb-2" />
          <p className="font-medium text-slate-700">Insurance</p>
        </Link>
        <Link to="/executive" className="card hover:shadow-md transition text-center">
          <BarChart3 className="w-8 h-8 text-accent-orange mx-auto mb-2" />
          <p className="font-medium text-slate-700">Executive</p>
        </Link>
      </div>
    </div>
  )
}