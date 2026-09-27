import { useEffect, useMemo, useState } from 'react'
import { Bell, Check, Plus, RefreshCw, Search } from 'lucide-react'
import { api } from '@/lib/api'
import { useSocket } from '@/hooks/useSocket'

const projectId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
const severityColors: Record<string, string> = { Low: 'bg-slate-100 text-slate-600', Medium: 'bg-yellow-100 text-yellow-700', High: 'bg-orange-100 text-orange-700', Critical: 'bg-red-100 text-red-700' }

export default function Alerts() {
  const [alerts, setAlerts] = useState<any[]>([])
  const [severity, setSeverity] = useState('all')
  const [status, setStatus] = useState('open')
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState<string[]>([])
  const [showCreate, setShowCreate] = useState(false)
  const [form, setForm] = useState({ alert_type: 'site_risk', severity: 3, severity_label: 'High', message: '' })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = () => { setLoading(true); api.get(`/projects/${projectId}/alerts`).then(response => setAlerts(response.data.data || [])).catch(() => setError('Alerts could not be loaded.')).finally(() => setLoading(false)) }
  useEffect(load, [])
  useSocket(projectId, load, load)

  const visible = useMemo(() => alerts.filter(alert => (severity === 'all' || alert.severity_label === severity) && (status === 'all' || (status === 'open' ? !alert.acknowledged : alert.acknowledged)) && `${alert.message} ${alert.source_agent}`.toLowerCase().includes(query.toLowerCase())), [alerts, severity, status, query])
  const acknowledge = async (id: string) => { await api.put(`/alerts/${id}/acknowledge`); setAlerts(current => current.map(alert => alert.alert_id === id ? { ...alert, acknowledged: true } : alert)); setSelected(current => current.filter(item => item !== id)) }
  const acknowledgeSelected = async () => { if (!selected.length) return; await api.post('/alerts/bulk-acknowledge', selected); setAlerts(current => current.map(alert => selected.includes(alert.alert_id) ? { ...alert, acknowledged: true } : alert)); setSelected([]) }
  const create = async () => { if (!form.message.trim()) return; const response = await api.post(`/projects/${projectId}/alerts`, { ...form, project_id: projectId, source_agent: 'Dashboard' }); setAlerts(current => [response.data.data, ...current]); setForm(current => ({ ...current, message: '' })); setShowCreate(false) }

  return <div>
    <div className="flex items-center justify-between mb-6"><div><h2 className="text-2xl font-bold text-slate-800">Alerts</h2><p className="mt-1 text-sm text-slate-500">Monitor, triage, acknowledge, and create operational alerts.</p></div><div className="flex gap-2"><button onClick={load} className="rounded-lg border border-slate-200 p-2 text-slate-600" aria-label="Refresh alerts"><RefreshCw className="h-4 w-4" /></button><button onClick={() => setShowCreate(current => !current)} className="flex items-center gap-2 rounded-lg bg-slate-900 px-3 py-2 text-sm font-semibold text-white"><Plus className="h-4 w-4" /> New alert</button></div></div>
    {showCreate && <div className="card mb-5"><div className="grid gap-3 md:grid-cols-3"><input value={form.alert_type} onChange={event => setForm({ ...form, alert_type: event.target.value })} className="rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="Alert type" /><select value={form.severity_label} onChange={event => setForm({ ...form, severity_label: event.target.value, severity: event.target.value === 'Critical' ? 4 : event.target.value === 'High' ? 3 : event.target.value === 'Medium' ? 2 : 1 })} className="rounded-lg border border-slate-200 px-3 py-2 text-sm"><option>Low</option><option>Medium</option><option>High</option><option>Critical</option></select><input value={form.message} onChange={event => setForm({ ...form, message: event.target.value })} className="rounded-lg border border-slate-200 px-3 py-2 text-sm md:col-span-3" placeholder="Describe the alert" /></div><button onClick={() => void create()} className="mt-3 rounded-lg bg-accent-orange px-4 py-2 text-sm font-semibold text-white">Create alert</button></div>}
    <div className="mb-5 flex flex-wrap gap-2"><div className="flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3"><Search className="h-4 w-4 text-slate-400" /><input value={query} onChange={event => setQuery(event.target.value)} className="w-48 py-2 text-sm outline-none" placeholder="Search alerts" /></div><select value={status} onChange={event => setStatus(event.target.value)} className="rounded-lg border border-slate-200 px-3 py-2 text-sm"><option value="open">Open</option><option value="acknowledged">Acknowledged</option><option value="all">All statuses</option></select><select value={severity} onChange={event => setSeverity(event.target.value)} className="rounded-lg border border-slate-200 px-3 py-2 text-sm"><option value="all">All severity</option><option>Critical</option><option>High</option><option>Medium</option><option>Low</option></select>{selected.length > 0 && <button onClick={() => void acknowledgeSelected()} className="rounded-lg bg-green-100 px-3 py-2 text-sm font-semibold text-green-700">Acknowledge {selected.length}</button>}</div>
    {error && <div className="mb-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
    {loading ? <p className="py-8 text-center text-slate-500">Loading alerts...</p> : <div className="space-y-3">{visible.map(alert => <div key={alert.alert_id} className={`card flex items-center justify-between gap-4 ${alert.acknowledged ? 'opacity-60' : ''}`}><div className="flex items-center gap-3"><input type="checkbox" checked={selected.includes(alert.alert_id)} onChange={event => setSelected(current => event.target.checked ? [...current, alert.alert_id] : current.filter(id => id !== alert.alert_id))} /><div className="flex h-10 w-10 items-center justify-center rounded-lg bg-red-100"><Bell className="h-5 w-5 text-red-600" /></div><div><div className="flex items-center gap-2"><span className={`rounded-full px-2 py-0.5 text-xs font-medium ${severityColors[alert.severity_label] || severityColors.Low}`}>{alert.severity_label}</span><span className="text-xs text-slate-400">{alert.source_agent}</span></div><p className="mt-1 text-sm text-slate-700">{alert.message}</p><p className="mt-1 text-xs text-slate-400">{new Date(alert.created_at).toLocaleString()}</p></div></div>{!alert.acknowledged && <button onClick={() => void acknowledge(alert.alert_id)} className="flex items-center gap-2 rounded-lg bg-green-100 px-3 py-2 text-sm font-medium text-green-700"><Check className="h-4 w-4" /> Acknowledge</button>}</div>)}{visible.length === 0 && <p className="py-8 text-center text-slate-500">No matching alerts.</p>}</div>}
  </div>
}
