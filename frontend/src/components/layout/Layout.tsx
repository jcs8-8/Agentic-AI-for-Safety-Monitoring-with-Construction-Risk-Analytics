import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopBar from './TopBar'
import CopilotChat from '@/components/copilot/CopilotChat'
import EmergencyMode from '@/components/emergency/EmergencyMode'
import { bindEmergencySocketEvents, useEmergencyStore } from '@/lib/emergency/emergencyStore'
import { useEffect } from 'react'

export default function Layout() {
  const emergencyState = useEmergencyStore(state => state.state)
  const report = useEmergencyStore(state => state.report)
  const dismissReport = useEmergencyStore(state => state.dismissReport)
  useEffect(() => { bindEmergencySocketEvents() }, [])
  return (
    <div className="flex h-screen bg-slate-50">
      {emergencyState === 'ACTIVE' || emergencyState === 'ACTIVATING' || emergencyState === 'CLOSING' ? <EmergencyMode /> : <><Sidebar /><div className="flex-1 flex flex-col overflow-hidden"><TopBar /><main className="flex-1 overflow-y-auto p-6"><Outlet /></main></div></>}
      <CopilotChat />
      {report && <div className="fixed inset-0 z-[90] flex items-center justify-center bg-slate-950/70 p-4"><div className="max-h-[85vh] w-full max-w-xl overflow-y-auto rounded-xl bg-white p-6"><div className="flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-widest text-red-600">Incident report generated</p><h2 className="text-xl font-bold text-slate-900">{report.id} · {report.incidentType}</h2></div><button onClick={dismissReport} className="rounded-lg p-2 text-slate-500 hover:bg-slate-100">×</button></div><p className="mt-3 text-sm text-slate-600">{report.zone} · {report.duration} · {report.timeline.length} timeline entries. {report.drill ? 'Tagged as drill and excluded from insurance statistics.' : 'Ready for insurer and regulator submission.'}</p><div className="mt-4 rounded-lg bg-slate-50 p-3 text-sm"><p className="font-semibold">Response summary</p><p className="mt-1 text-slate-600">Activated by {report.activatedBy}; closed by {report.closedBy}. Checklist completion: {report.checklist.filter(item => item.checked).length}/{report.checklist.length}.</p></div><div className="mt-5 flex gap-2"><a href="/incidents" onClick={dismissReport} className="flex-1 rounded-lg border border-slate-200 px-4 py-3 text-center text-sm font-semibold text-slate-700">Open incident archive</a><button onClick={dismissReport} className="flex-1 rounded-lg bg-red-600 px-4 py-3 text-sm font-bold text-white">Done</button></div></div></div>}
    </div>
  )
}