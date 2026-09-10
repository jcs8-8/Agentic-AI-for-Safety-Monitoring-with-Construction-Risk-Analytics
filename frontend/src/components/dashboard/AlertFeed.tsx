interface Alert { alert_id: string; message: string; severity: number; severity_label: string; created_at: string; source_agent: string }
interface Props { alerts: Alert[] }

const severityColors: Record<string, string> = {
  'Low': 'bg-slate-100 text-slate-600',
  'Medium': 'bg-yellow-100 text-yellow-700',
  'High': 'bg-orange-100 text-orange-700',
  'Critical': 'bg-red-100 text-red-700'
}

export default function AlertFeed({ alerts }: Props) {
  return (
    <div className="card">
      <h3 className="font-bold text-slate-800 mb-4 text-sm">Recent Alerts</h3>
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {alerts.map((a) => (
          <div key={a.alert_id} className="p-3 bg-slate-50 rounded-lg">
            <div className="flex items-center justify-between mb-1">
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${severityColors[a.severity_label] || severityColors['Low']}`}>
                {a.severity_label}
              </span>
              <span className="text-xs text-slate-400">{a.source_agent}</span>
            </div>
            <p className="text-sm text-slate-700">{a.message}</p>
          </div>
        ))}
      </div>
    </div>
  )
}