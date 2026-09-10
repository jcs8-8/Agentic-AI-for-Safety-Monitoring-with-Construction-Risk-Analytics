import { useState } from 'react'
import { Bell, ChevronDown, Activity } from 'lucide-react'

export default function TopBar() {
  const [project] = useState('Downtown High-Rise Tower')
  return (
    <header className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <button className="flex items-center gap-2 px-4 py-2 bg-slate-100 rounded-lg text-sm font-medium hover:bg-slate-200 transition">
          {project}
          <ChevronDown className="w-4 h-4" />
        </button>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 text-green-700 rounded-full text-sm font-medium">
          <Activity className="w-4 h-4 animate-pulse" />
          Live Monitoring
        </div>
        <button className="relative p-2 text-slate-500 hover:text-slate-700 transition">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-status-danger rounded-full"></span>
        </button>
      </div>
    </header>
  )
}