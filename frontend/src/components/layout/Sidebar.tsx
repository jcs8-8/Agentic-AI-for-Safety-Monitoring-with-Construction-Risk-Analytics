import { NavLink, useLocation } from 'react-router-dom'
import { Home, AlertTriangle, Shield, ClipboardCheck, Umbrella, BarChart3, Bot, FileText, Bell, Settings, Building2, Workflow } from 'lucide-react'

const navItems = [
  { path: '/', label: 'Dashboard', icon: Home },
  { path: '/site-risk', label: 'Site Risk', icon: AlertTriangle },
  { path: '/safety', label: 'Safety', icon: Shield },
  { path: '/compliance', label: 'Compliance', icon: ClipboardCheck },
  { path: '/insurance', label: 'Insurance', icon: Umbrella },
  { path: '/executive', label: 'Executive', icon: BarChart3 },
  { path: '/agents', label: 'Agents', icon: Bot },
  { path: '/reports', label: 'Reports', icon: FileText },
  { path: '/alerts', label: 'Alerts', icon: Bell },
  { path: '/settings', label: 'Settings', icon: Settings },
  { path: '/architecture', label: 'Architecture', icon: Workflow },
]

export default function Sidebar() {
  const location = useLocation()
  return (
    <aside className="w-64 bg-primary-navy text-white flex flex-col flex-shrink-0">
      <div className="p-5 flex items-center gap-3 border-b border-slate-700">
        <Building2 className="w-8 h-8 text-accent-orange" />
        <div>
          <h1 className="font-bold text-lg leading-tight">BuildSure AI</h1>
          <p className="text-xs text-slate-400">Risk Intelligence</p>
        </div>
      </div>
      <nav className="flex-1 py-4 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path || location.pathname.startsWith(item.path + '/')
          return (
            <NavLink key={item.path} to={item.path}
              className={`flex items-center gap-3 px-5 py-3 text-sm transition-colors ${isActive ? 'bg-accent-orange text-white' : 'text-slate-300 hover:bg-slate-700 hover:text-white'}`}>
              <item.icon className="w-5 h-5" />
              {item.label}
            </NavLink>
          )
        })}
      </nav>
      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-accent-blue flex items-center justify-center text-sm font-bold">JD</div>
          <div>
            <p className="text-sm font-medium">John Doe</p>
            <p className="text-xs text-slate-400">Site Manager</p>
          </div>
        </div>
      </div>
    </aside>
  )
}