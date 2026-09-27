export type EmergencyState = 'IDLE' | 'ACTIVATING' | 'ACTIVE' | 'CLOSING' | 'CLOSED'
export type IncidentType = 'Injury' | 'Structural' | 'Fire' | 'Gas Leak' | 'Other'
export type UserRole = 'SITE_MANAGER' | 'SAFETY_OFFICER' | 'EXECUTIVE' | 'WORKER'
export type Milestone = 'Evacuation started' | 'EMS called' | 'Area secured' | 'All clear'

export interface EmergencyAlert { id: string; source: string; severity: 'Critical' | 'High' | 'Medium'; message: string; timestamp: string }
export interface TimelineEntry { id: string; kind: 'system' | 'alert' | 'note' | 'camera'; text: string; author: string; timestamp: string; milestone?: Milestone; photoName?: string }
export interface ChecklistItem { id: string; label: string; assignee: string; checked: boolean; checkedAt?: string }
export interface CameraFeed { id: string; name: string; zone: string; frame: number; recording: boolean }
export interface NotificationStatus { smsSent: number; smsTotal: number; teams: 'posted' | 'pending'; siren: boolean; undelivered: number }
export interface EmergencySession {
  id: string
  incidentId: string
  incidentType: IncidentType
  zone: string
  state: EmergencyState
  activatedAt: string
  activatedBy: string
  closedAt?: string
  closedBy?: string
  closeReason?: string
  drill?: boolean
  timeline: TimelineEntry[]
  checklist: ChecklistItem[]
  cameras: CameraFeed[]
  notifications: NotificationStatus
}

export interface IncidentReport { id: string; sessionId: string; incidentType: IncidentType; zone: string; duration: string; activatedBy: string; closedBy: string; timeline: TimelineEntry[]; checklist: ChecklistItem[]; alerts: EmergencyAlert[]; cameras: CameraFeed[]; notifications: NotificationStatus; drill: boolean; generatedAt: string }
