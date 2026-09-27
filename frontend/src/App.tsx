import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import SiteRiskDashboard from './pages/SiteRiskDashboard'
import SafetyDashboard from './pages/SafetyDashboard'
import ComplianceDashboard from './pages/ComplianceDashboard'
import InsuranceDashboard from './pages/InsuranceDashboard'
import ExecutiveDashboard from './pages/ExecutiveDashboard'
import AgentOrchestrator from './pages/AgentOrchestrator'
import Reports from './pages/Reports'
import Alerts from './pages/Alerts'
import Login from './pages/Login'
import Architecture from './pages/Architecture'
import Incidents from './pages/Incidents'
import Settings from './pages/Settings'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/site-risk/:projectId?" element={<SiteRiskDashboard />} />
        <Route path="/safety/:projectId?" element={<SafetyDashboard />} />
        <Route path="/compliance/:projectId?" element={<ComplianceDashboard />} />
        <Route path="/insurance/:projectId?" element={<InsuranceDashboard />} />
        <Route path="/executive/:projectId?" element={<ExecutiveDashboard />} />
        <Route path="/agents" element={<AgentOrchestrator />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/architecture" element={<Architecture />} />
        <Route path="/incidents" element={<Incidents />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  )
}
export default App