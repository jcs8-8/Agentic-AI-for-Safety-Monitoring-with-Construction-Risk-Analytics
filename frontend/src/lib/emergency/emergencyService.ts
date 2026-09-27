import { api } from '@/lib/api'
import { socket } from '@/lib/socket'
import type { EmergencySession, IncidentReport, IncidentType, TimelineEntry } from './types'

const mode = import.meta.env.VITE_EMERGENCY_MODE || 'mock'
const projectId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
const time = () => new Date().toISOString()
const templates: Record<IncidentType, string> = { Injury: 'Call site medic and 108 ambulance. Secure the affected area immediately.', Structural: 'STOP WORK. Evacuate the affected zone and report to the muster point.', Fire: 'EVACUATE immediately. Do not re-enter until cleared by emergency services.', 'Gas Leak': 'EVACUATE upwind. Do not use electrical switches or ignition sources.', Other: 'Follow the site emergency plan and report to the muster point.' }

function mockSession(type: IncidentType, zone: string, user: string): EmergencySession {
  const activatedAt = time()
  const checklistLabels: Record<IncidentType, string[]> = {
    Injury: ['Call site medic / 108 ambulance', `Secure the area — cordon off ${zone}`, 'Stop all work in adjacent zones', 'Notify site manager + safety officer', 'Start incident timeline recording', 'Preserve camera footage'],
    Structural: ['Stop work and evacuate affected zone', 'Account for all workers at muster point', 'Notify structural engineer and site manager', 'Cordon off the collapse area', 'Preserve camera footage', 'Contact emergency services'],
    Fire: ['Activate fire alarm and call emergency services', 'Evacuate workers to muster point', 'Account for all personnel', 'Isolate utilities if safe', 'Notify site manager + safety officer', 'Preserve camera footage'],
    'Gas Leak': ['Stop work and isolate ignition sources', 'Evacuate upwind to muster point', 'Call emergency services', 'Account for all personnel', 'Cordon off the leak area', 'Preserve camera footage'],
    Other: ['Assess and secure the affected area', 'Notify site manager + safety officer', 'Account for all personnel', 'Start incident timeline recording', 'Preserve camera footage', 'Contact emergency services'],
  }
  return { id: `session-${Date.now()}`, incidentId: `INC-2026-${String(Math.floor(Math.random() * 900) + 100)}`, incidentType: type, zone, state: 'ACTIVE', activatedAt, activatedBy: user, timeline: [{ id: `entry-${Date.now()}`, kind: 'system', text: `${type} emergency activated in ${zone}.`, author: user, timestamp: activatedAt }], checklist: checklistLabels[type].map((label, index) => ({ id: `check-${index}`, label, assignee: 'Unassigned', checked: false })), cameras: Array.from({ length: 8 }, (_, index) => ({ id: `camera-${index + 1}`, name: `Camera ${index + 1}`, zone: index < 3 ? zone : `Zone ${String.fromCharCode(65 + (index % 4))}`, frame: 0, recording: false })), notifications: { smsSent: 34, smsTotal: 45, teams: 'posted', siren: true, undelivered: 11 } }
}

export async function activateEmergency(type: IncidentType, zone: string, user: string): Promise<EmergencySession> {
  if (mode === 'live') return (await api.post('/emergencies', { incident_type: type, zone, activated_by: user, project_id: projectId })).data.data
  const session = mockSession(type, zone, user)
  socket.emit('EMERGENCY_ACTIVATED', session)
  return session
}

export async function updateEmergency(session: EmergencySession): Promise<void> {
  if (mode === 'live') await api.put(`/emergencies/${session.id}`, session)
  socket.emit('EMERGENCY_UPDATED', session)
}

export async function deactivateEmergency(session: EmergencySession, reason: string, user: string, drill: boolean): Promise<IncidentReport> {
  if (mode === 'live') return (await api.post(`/emergencies/${session.id}/close`, { reason, closed_by: user, drill })).data.data
  const closedAt = time()
  const duration = `${Math.max(1, Math.round((new Date(closedAt).getTime() - new Date(session.activatedAt).getTime()) / 60000))} min`
  const report: IncidentReport = { id: session.incidentId, sessionId: session.id, incidentType: session.incidentType, zone: session.zone, duration, activatedBy: session.activatedBy, closedBy: user, timeline: [...session.timeline, { id: `entry-${Date.now()}`, kind: 'system', text: `Emergency closed: ${reason}`, author: user, timestamp: closedAt }], checklist: session.checklist, alerts: [{ id: 'emergency-alert-1', source: 'Safety Agent', severity: 'Critical', message: `${session.incidentType} response alert in ${session.zone}`, timestamp: session.activatedAt }], cameras: session.cameras, notifications: session.notifications, drill, generatedAt: closedAt }
  socket.emit('EMERGENCY_DEACTIVATED', report)
  return report
}

export async function requestEmergencyActivation(type: IncidentType, zone: string, requester: string): Promise<void> {
  if (mode === 'live') await api.post('/emergencies/request', { incident_type: type, zone, requester, project_id: projectId })
  socket.emit('EMERGENCY_ACTIVATION_REQUESTED', { type, zone, requester })
}

export function broadcastTemplate(type: IncidentType): string { return templates[type] }
export function listenForEmergencyEvents(onActivate: (session: EmergencySession) => void, onDeactivate: (report: IncidentReport) => void): () => void { socket.on('EMERGENCY_ACTIVATED', onActivate); socket.on('EMERGENCY_DEACTIVATED', onDeactivate); return () => { socket.off('EMERGENCY_ACTIVATED', onActivate); socket.off('EMERGENCY_DEACTIVATED', onDeactivate) } }
export function addTimelineEntry(session: EmergencySession, entry: Omit<TimelineEntry, 'id' | 'timestamp'>): EmergencySession { return { ...session, timeline: [...session.timeline, { ...entry, id: `entry-${Date.now()}`, timestamp: time() }] } }