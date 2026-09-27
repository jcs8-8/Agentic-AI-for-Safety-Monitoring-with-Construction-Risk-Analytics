import { useEffect, useMemo, useState } from 'react'
import { AlertOctagon, Download, FileText, Plus, Search } from 'lucide-react'
import { jsPDF } from 'jspdf'
import { api } from '@/lib/api'
import { useEmergencyStore } from '@/lib/emergency/emergencyStore'
import type { IncidentReport } from '@/lib/emergency/types'

const projectId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
const incidentTypes = ['Injury', 'Structural', 'Fire', 'Gas Leak', 'Other']

function downloadEmergency(report: IncidentReport) {
  const pdf = new jsPDF()
  pdf.setFontSize(16)
  pdf.text(`${report.id} - Emergency Incident Report`, 18, 18)
  pdf.setFontSize(10)
  pdf.text(`${report.incidentType} | ${report.zone} | ${report.duration}`, 18, 28)
  pdf.text(`Activated by ${report.activatedBy}; closed by ${report.closedBy}`, 18, 36)
  pdf.text(`Classification: ${report.drill ? 'DRILL' : 'Operational incident'}`, 18, 44)
  pdf.save(`${report.id}.pdf`)
}

export default function Incidents() {
  const archive = useEmergencyStore(state => state.archive)
  const [incidents, setIncidents] = useState<any[]>([])
  const [status, setStatus] = useState('all')
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState<any>()
  const [showCreate, setShowCreate] = useState(false)
  const [form, setForm] = useState({ incident_type: 'Injury', severity: 3, incident_date: new Date().toISOString().slice(0, 16), description: '', location_zone: 'Zone B', worker_name: '', ppe_involved: false, status: 'open' })
  const [error, setError] = useState('')

  const load = () => api.get(`/projects/${projectId}/safety/incidents`).then(response => setIncidents(response.data.data || [])).catch(() => setError('Incidents could not be loaded.'))
  useEffect(() => { void load() }, [])
  const visible = useMemo(() => incidents.filter(item => (status === 'all' || item.status === status) && `${item.type} ${item.description} ${item.location}`.toLowerCase().includes(query.toLowerCase())), [incidents, status, query])
  const create = async () => {
    if (!form.description.trim()) return
    try { await api.post(`/projects/${projectId}/safety/incidents`, { ...form, incident_date: new Date(form.incident_date).toISOString(), project_id: projectId }); await load(); setShowCreate(false); setForm(current => ({ ...current, description: '', worker_name: '' })) }
    catch { setError('Incident could not be recorded.') }
  }
  const updateStatus = async (id: string, nextStatus: string) => { await api.put(`/safety/incidents/${id}/status?status=${nextStatus}`); setIncidents(current => current.map(item => item.incident_id === id ? { ...item, status: nextStatus } : item)) }

  return <div>
    <div className="mb-6 flex items-center justify-between"><div><h2 className="text-2xl font-bold text-slate-800">Incident management</h2><p className="mt-1 text-sm text-slate-500">Record, investigate, resolve, and archive safety events.</p></div><div className="flex gap-2"><AlertOctagon className="h-8 w-8 text-red-600" /><button onClick={() => setShowCreate(current => !current)} className="flex items-center gap-2 rounded-lg bg-red-600 px-3 py-2 text-sm font-semibold text-white"><Plus className="h-4 w-4" /> Record incident</button></div></div>
    {showCreate && <div className="card mb-5"><div className="grid gap-3 md:grid-cols-3"><select value={form.incident_type} onChange={event => setForm({ ...form, incident_type: event.target.value })} className="rounded-lg border border-slate-200 px-3 py-2 text-sm">{incidentTypes.map(item => <option key={item}>{item}</option>)}</select><select value={form.severity} onChange={event => setForm({ ...form, severity: Number(event.target.value) })} className="rounded-lg border border-slate-200 px-3 py-2 text-sm"><option value="1">Low severity</option><option value="2">Medium severity</option><option value="3">High severity</option><option value="4">Critical severity</option><option value="5">Extreme severity</option></select><input type="datetime-local" value={form.incident_date} onChange={event => setForm({ ...form, incident_date: event.target.value })} className="rounded-lg border border-slate-200 px-3 py-2 text-sm" /><input value={form.location_zone} onChange={event => setForm({ ...form, location_zone: event.target.value })} className="rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="Location / zone" /><input value={form.worker_name} onChange={event => setForm({ ...form, worker_name: event.target.value })} className="rounded-lg border border-slate-200 px-3 py-2 text-sm" placeholder="Worker name (optional)" /><label className="flex items-center gap-2 text-sm text-slate-600"><input type="checkbox" checked={form.ppe_involved} onChange={event => setForm({ ...form, ppe_involved: event.target.checked })} /> PPE involved</label><textarea value={form.description} onChange={event => setForm({ ...form, description: event.target.value })} className="rounded-lg border border-slate-200 px-3 py-2 text-sm md:col-span-3" placeholder="Describe what happened" /></div><button onClick={() => void create()} className="mt-3 rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white">Save incident</button></div>}
    <div className="mb-5 flex flex-wrap gap-2"><div className="flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3"><Search className="h-4 w-4 text-slate-400" /><input value={query} onChange={event => setQuery(event.target.value)} className="w-48 py-2 text-sm outline-none" placeholder="Search incidents" /></div><select value={status} onChange={event => setStatus(event.target.value)} className="rounded-lg border border-slate-200 px-3 py-2 text-sm"><option value="all">All statuses</option><option value="open">Open</option><option value="investigating">Investigating</option><option value="resolved">Resolved</option><option value="closed">Closed</option></select></div>
    {error && <div className="mb-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
    <div className="space-y-3">{visible.map(item => <div key={item.incident_id} className="card flex items-center justify-between gap-4"><div><div className="flex items-center gap-2"><span className="font-bold text-slate-800">{item.type}</span><span className="rounded-full bg-red-100 px-2 py-0.5 text-xs font-semibold text-red-700">Severity {item.severity}</span><span className="text-xs text-slate-400">{item.status}</span></div><p className="mt-1 text-sm text-slate-600">{item.description}</p><p className="mt-1 text-xs text-slate-400">{item.location || 'Location unavailable'} · {new Date(item.date).toLocaleString()}</p></div><div className="flex gap-2"><button onClick={() => setSelected(item)} className="rounded-lg bg-slate-100 px-3 py-2 text-xs font-semibold text-slate-700">Details</button><select value={item.status} onChange={event => void updateStatus(item.incident_id, event.target.value)} className="rounded-lg border border-slate-200 px-2 py-2 text-xs"><option>open</option><option>investigating</option><option>resolved</option><option>closed</option></select></div></div>)}{visible.length === 0 && <p className="py-8 text-center text-slate-500">No matching incidents.</p>}{archive.map(report => <div key={report.id} className="card flex items-center justify-between gap-4"><div className="flex items-center gap-3"><FileText className="h-5 w-5 text-red-600" /><div><p className="font-bold text-slate-800">{report.id} · {report.incidentType}</p><p className="text-sm text-slate-500">Emergency report · {report.zone} · {report.duration}{report.drill ? ' · DRILL' : ''}</p></div></div><button onClick={() => downloadEmergency(report)} className="rounded-lg bg-red-600 p-2 text-white" aria-label="Download emergency report"><Download className="h-4 w-4" /></button></div>)}</div>
    {selected && <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4" onClick={() => setSelected(undefined)}><div className="w-full max-w-xl rounded-xl bg-white p-6" onClick={event => event.stopPropagation()}><h3 className="font-bold text-slate-800">Incident details</h3><p className="mt-4 text-sm text-slate-600">{selected.description}</p><dl className="mt-4 grid grid-cols-2 gap-3 text-sm"><div><dt className="text-slate-400">Worker</dt><dd>{selected.worker || 'Not recorded'}</dd></div><div><dt className="text-slate-400">Location</dt><dd>{selected.location || 'Not recorded'}</dd></div><div><dt className="text-slate-400">Status</dt><dd>{selected.status}</dd></div><div><dt className="text-slate-400">PPE involved</dt><dd>{selected.ppe_involved ? 'Yes' : 'No'}</dd></div></dl></div></div>}
  </div>
}
