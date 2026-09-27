import { api } from '@/lib/api'
import type { CopilotAction, CopilotMessage, CopilotResponse } from './tools'

const mode = import.meta.env.VITE_COPILOT_MODE || 'mock'
const now = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

const alerts = [
  { id: 'alert-zone-b-ppe', severity: 'Critical' as const, message: 'PPE violation detected near the material hoist.', zone: 'Zone B', source: 'Safety Agent', createdAt: 'Today, 13:28', acknowledged: false },
  { id: 'alert-crane-3', severity: 'High' as const, message: 'Unsecured load proximity alert near Crane 3.', zone: 'Zone C', source: 'Site Risk Agent', createdAt: 'Today, 12:54', acknowledged: false },
  { id: 'alert-scaffold', severity: 'High' as const, message: 'Scaffolding inspection is overdue by 2 hours.', zone: 'Zone A', source: 'Compliance Agent', createdAt: 'Today, 10:02', acknowledged: true },
]

function source(tool: string) {
  const names: Record<string, string> = { query_alerts: 'Safety Agent', get_risk_scores: 'Risk Intelligence Engine', get_analytics: 'Reporting Agent', get_predictions: 'Risk Intelligence Engine', generate_report: 'Reporting Agent' }
  return names[tool] || 'BuildSure AI'
}

export async function sendCopilotMessage(text: string, history: CopilotMessage[] = []): Promise<CopilotResponse> {
  if (mode === 'live') {
    const response = await api.post('/copilot/chat', { message: text, history })
    return response.data.data
  }
  const emergencyData = localStorage.getItem('buildsure-emergency-state')
  if (emergencyData) {
    try { const emergency = JSON.parse(emergencyData).state; if (emergency?.session && /worker|headcount|zone b|activation/.test(text.toLowerCase())) return { tool: 'query_alerts', text: `Emergency context: the current response is for ${emergency.session.incidentType} in ${emergency.session.zone}. Mock activation headcount is 42 workers; verify against the site roll call.`, source: 'Safety Agent', asOf: now() } } catch { /* local session may be incomplete */ }
  }
  return mockResponse(text)
}

export async function executeCopilotAction(action: CopilotAction): Promise<CopilotResponse> {
  if (mode === 'live') {
    const response = await api.post('/copilot/action', { ...action, role: localStorage.getItem('buildsure_role') || 'site_manager' })
    return response.data.data
  }
  return { tool: action.tool, text: action.tool === 'dismiss_alert' ? 'The alert was dismissed and the audit event was recorded.' : 'The action was completed and the workflow has been updated.' }
}

function mockResponse(input: string): CopilotResponse {
  const text = input.toLowerCase()
  const asOf = now()
  if (/assign|escalate|false positive|dismiss|mark .*alert/.test(text)) {
    const tool = text.includes('assign') ? 'assign_alert' : text.includes('escalate') ? 'escalate_alert' : 'dismiss_alert'
    const role = localStorage.getItem('buildsure_role') || 'site_manager'
    if (tool === 'dismiss_alert' && role.toLowerCase() === 'executive') return { tool, text: 'Your EXECUTIVE role can view and escalate alerts, but cannot dismiss them.' }
    return { tool, text: 'This workflow change needs your confirmation before it runs.', source: 'Alert Management', asOf, widget: { type: 'confirm', action: { tool, alertId: alerts[0].id, assignee: text.includes('rajesh') ? 'Rajesh' : undefined, reason: input }, label: tool === 'dismiss_alert' ? 'Dismiss alert' : tool === 'assign_alert' ? 'Assign alert' : 'Escalate alerts', detail: input } }
  }
  if (/risk score|riskiest|risk today|current project risk/.test(text)) return { tool: 'get_risk_scores', text: 'The current project risk score is 78/100. Zone B is the riskiest area today.', source: source('get_risk_scores'), asOf, widget: { type: 'risk', score: 78, zones: [{ name: 'Zone B', score: 62, openHazards: 7 }, { name: 'Zone C', score: 74, openHazards: 4 }, { name: 'Zone A', score: 86, openHazards: 2 }] } }
  if (/trend|compare|compliance|time of day|weekly/.test(text)) return { tool: 'get_analytics', text: 'Safety compliance improved 8 points this month compared with last month, with the largest hazard peak during the 14:00 shift.', source: source('get_analytics'), asOf, widget: { type: 'chart', chart: text.includes('time') ? 'bar' : 'line', title: text.includes('time') ? 'Hazards by time of day' : 'Safety compliance trend', xKey: 'period', yKeys: ['current', 'previous'], data: [{ period: 'Mon', current: 86, previous: 78 }, { period: 'Tue', current: 89, previous: 80 }, { period: 'Wed', current: 91, previous: 83 }, { period: 'Thu', current: 88, previous: 82 }, { period: 'Fri', current: 94, previous: 86 }] } }
  if (/forecast|tomorrow|exposure|scaffolding/.test(text)) return { tool: 'get_predictions', text: 'Tomorrow night shift is forecast at elevated exposure because scaffolding hazards remain open.', source: source('get_predictions'), asOf, widget: { type: 'forecast', title: 'Night shift risk forecast', value: 'Elevated · 71/100', confidence: '87% confidence', actions: ['Close or isolate the 3 scaffolding hazards before 19:00.', 'Add a supervisor walkthrough at shift handover.'] } }
  if (/report|executive summary|email/.test(text)) return { tool: 'generate_report', text: 'I prepared a report preview using yesterday’s site activity and alert data.', source: source('generate_report'), asOf, widget: { type: 'report', title: 'Yesterday site report', period: '18 Sep 2026', reportId: 'site-report-2026-09-18', highlights: ['3 critical alerts reviewed', 'Safety compliance: 91%', 'No recordable incidents'] } }
  if (/critical|ppe|alert|incident|crane|zone b/.test(text)) return { tool: 'query_alerts', text: 'I found 2 open high-severity alerts matching the current platform data.', source: source('query_alerts'), asOf, widget: { type: 'alerts', alerts: alerts.filter(alert => !alert.acknowledged) } }
  if (/what can you do|help|hello|hi\b/.test(text)) return { tool: 'small_talk', text: 'I can query live alerts, explain risk scores, compare trends, forecast exposure, generate reports, and prepare workflow actions for confirmation.' }
  return { tool: 'small_talk', text: 'I can only answer from BuildSure platform data. Try asking about open alerts, today’s risk score, a weekly trend, a forecast, or a site report.' }
}