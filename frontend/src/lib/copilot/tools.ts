export type CopilotTool =
  | 'query_alerts'
  | 'get_risk_scores'
  | 'get_analytics'
  | 'get_predictions'
  | 'generate_report'
  | 'assign_alert'
  | 'escalate_alert'
  | 'create_task'
  | 'dismiss_alert'
  | 'small_talk'

export type CopilotWidget =
  | { type: 'alerts'; alerts: AlertWidget[] }
  | { type: 'risk'; score: number; zones: ZoneWidget[] }
  | { type: 'chart'; chart: 'line' | 'bar'; title: string; data: Record<string, string | number>[]; xKey: string; yKeys: string[] }
  | { type: 'forecast'; title: string; value: string; confidence: string; actions: string[] }
  | { type: 'report'; title: string; period: string; highlights: string[]; reportId: string }
  | { type: 'confirm'; action: CopilotAction; label: string; detail: string }
  | { type: 'zones'; zones: ZoneWidget[] }

export interface AlertWidget {
  id: string
  severity: 'Low' | 'Medium' | 'High' | 'Critical'
  message: string
  zone: string
  source: string
  createdAt: string
  acknowledged: boolean
}

export interface ZoneWidget { name: string; score: number; openHazards: number }

export interface CopilotAction {
  tool: 'assign_alert' | 'escalate_alert' | 'create_task' | 'dismiss_alert'
  alertId?: string
  assignee?: string
  reason?: string
}

export interface CopilotMessage {
  id: string
  role: 'user' | 'assistant'
  text: string
  createdAt: string
  source?: string
  asOf?: string
  tool?: CopilotTool
  widget?: CopilotWidget
  status?: 'pending' | 'complete' | 'error'
}

export interface CopilotResponse {
  text: string
  source?: string
  asOf?: string
  tool: CopilotTool
  widget?: CopilotWidget
}

export const copilotToolSchemas = {
  query_alerts: { name: 'query_alerts', description: 'Query platform alerts and incidents by severity, zone, type, or time.', parameters: { type: 'object', properties: { zone: { type: 'string' }, severity: { type: 'string' }, period: { type: 'string' } } } },
  get_risk_scores: { name: 'get_risk_scores', description: 'Get current project and zone risk scores from the Risk Intelligence Engine.', parameters: { type: 'object', properties: { projectId: { type: 'string' } } } },
  get_analytics: { name: 'get_analytics', description: 'Compare safety, compliance, and hazard trends from platform data.', parameters: { type: 'object', properties: { metric: { type: 'string' }, period: { type: 'string' } } } },
  get_predictions: { name: 'get_predictions', description: 'Return a forecast or what-if exposure from the Risk Intelligence Engine.', parameters: { type: 'object', properties: { scenario: { type: 'string' } } } },
  generate_report: { name: 'generate_report', description: 'Generate a site or executive report from platform data.', parameters: { type: 'object', properties: { period: { type: 'string' }, audience: { type: 'string' } } } },
  assign_alert: { name: 'assign_alert', description: 'Assign an alert after explicit user confirmation.', parameters: { type: 'object', properties: { alertId: { type: 'string' }, assignee: { type: 'string' } }, required: ['alertId', 'assignee'] } },
  escalate_alert: { name: 'escalate_alert', description: 'Escalate alerts after explicit user confirmation.', parameters: { type: 'object', properties: { alertId: { type: 'string' }, reason: { type: 'string' } } } },
  create_task: { name: 'create_task', description: 'Create a follow-up task after explicit user confirmation.', parameters: { type: 'object', properties: { reason: { type: 'string' } }, required: ['reason'] } },
  dismiss_alert: { name: 'dismiss_alert', description: 'Dismiss an alert after explicit user confirmation and role authorization.', parameters: { type: 'object', properties: { alertId: { type: 'string' }, reason: { type: 'string' } }, required: ['alertId'] } },
} as const