import { LucideIcon } from 'lucide-react'

interface KpiCardProps {
  label: string; value: string; icon: LucideIcon; color: string; trend?: string
}

export default function KpiCard({ label, value, icon: Icon, color, trend }: KpiCardProps) {
  return (
    <div className="card flex items-center gap-4">
      <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ backgroundColor: `${color}15` }}>
        <Icon className="w-6 h-6" style={{ color }} />
      </div>
      <div>
        <p className="kpi-label">{label}</p>
        <p className="kpi-value">{value}</p>
        {trend && <p className="text-xs text-status-success font-medium">{trend}</p>}
      </div>
    </div>
  )
}