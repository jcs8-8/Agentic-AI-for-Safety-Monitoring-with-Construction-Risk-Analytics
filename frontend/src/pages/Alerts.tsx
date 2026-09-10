import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { Bell, Check } from 'lucide-react'
import { useSocket } from '@/hooks/useSocket'

export default function Alerts() {
  const [alerts, setAlerts] = useState<any[]>([])
  const projectId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'

  useEffect(() => {
    api.get(`/projects/${projectId}/alerts`).then(r => setAlerts(r.data.data))
  }, [])

  useSocket(projectId, () => {
    api.get(`/projects/${projectId}/alerts`).then(r => setAlerts(r.data.data))
  }, () => {
    api.get(`/projects/${projectId}/alerts`).then(r => setAlerts(r.data.data))
  })

  const acknowledge = async (id: string) => {
    await api.put(`/alerts/${id}/acknowledge`)
    setAlerts(current => current.map(a => a.alert_id === id ? { ...a, acknowledged: true } : a))
  }

  const severityColors: Record<string, string> = {
    'Low': 'bg-slate-100 text-slate-600',
    'Medium': 'bg-yellow-100 text-yellow-700',
    'High': 'bg-orange-100 text-orange-700',
    'Critical': 'bg-red-100 text-red-700'
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Alerts</h2>
      <div className="space-y-3">
        {alerts.map((alert) => (
          <div key={alert.alert_id} className={`card flex items-center justify-between ${alert.acknowledged ? 'opacity-60' : ''}`}>
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center">
                <Bell className="w-5 h-5 text-red-600" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${severityColors[alert.severity_label] || severityColors['Low']}`}>
                    {alert.severity_label}
                  </span>
                  <span className="text-xs text-slate-400">{alert.source_agent}</span>
                </div>
                <p className="text-sm text-slate-700 mt-1">{alert.message}</p>
              </div>
            </div>
            {!alert.acknowledged && (
              <button onClick={() => acknowledge(alert.alert_id)}
                className="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-lg text-sm font-medium hover:bg-green-200 transition">
                <Check className="w-4 h-4" /> Acknowledge
              </button>
            )}
          </div>
        ))}
        {alerts.length === 0 && <p className="text-slate-500 text-center py-8">No alerts.</p>
        }
      </div>
    </div>
  )
}