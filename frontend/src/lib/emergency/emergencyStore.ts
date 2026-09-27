import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { activateEmergency, addTimelineEntry, deactivateEmergency, listenForEmergencyEvents, requestEmergencyActivation, updateEmergency } from './emergencyService'
import type { EmergencySession, IncidentReport, IncidentType, TimelineEntry, UserRole } from './types'

interface EmergencyState {
  state: EmergencySession['state']
  session?: EmergencySession
  report?: IncidentReport
  archive: IncidentReport[]
  activationRequested: boolean
  activate: (type: IncidentType, zone: string, user: string, role: UserRole) => Promise<boolean>
  requestActivation: (type: IncidentType, zone: string, user: string) => Promise<void>
  updateChecklist: (id: string, checked: boolean, assignee: string) => Promise<void>
  addEntry: (entry: Omit<TimelineEntry, 'id' | 'timestamp'>) => Promise<void>
  toggleRecording: (cameraId: string) => Promise<void>
  setSiren: (on: boolean) => Promise<void>
  close: (reason: string, user: string, drill: boolean) => Promise<void>
  dismissReport: () => void
}

export const useEmergencyStore = create<EmergencyState>()(persist((set, get) => ({
  state: 'IDLE', archive: [], activationRequested: false,
  activate: async (type, zone, user, role) => { if (role !== 'SITE_MANAGER' && role !== 'SAFETY_OFFICER') return false; set({ state: 'ACTIVATING' }); const session = await activateEmergency(type, zone, user); set({ state: 'ACTIVE', session }); return true },
  requestActivation: async (type, zone, user) => { await requestEmergencyActivation(type, zone, user); set({ activationRequested: true }) },
  updateChecklist: async (id, checked, assignee) => { const session = get().session; if (!session) return; const checklist = session.checklist.map(item => item.id === id ? { ...item, checked, assignee, checkedAt: checked ? new Date().toISOString() : undefined } : item); const updated = { ...session, checklist }; set({ session: updated }); await updateEmergency(updated) },
  addEntry: async (entry) => { const session = get().session; if (!session) return; const updated = addTimelineEntry(session, entry); set({ session: updated }); await updateEmergency(updated) },
  toggleRecording: async (cameraId) => { const session = get().session; if (!session) return; const cameras = session.cameras.map(camera => camera.id === cameraId ? { ...camera, recording: !camera.recording } : camera); const updated = { ...session, cameras }; set({ session: updated }); await updateEmergency(updated) },
  setSiren: async (on) => { const session = get().session; if (!session) return; const updated = { ...session, notifications: { ...session.notifications, siren: on } }; set({ session: updated }); await updateEmergency(updated) },
  close: async (reason, user, drill) => { const session = get().session; if (!session || !reason.trim()) return; set({ state: 'CLOSING' }); const report = await deactivateEmergency(session, reason, user, drill); set(state => ({ state: 'CLOSED', report, session: undefined, archive: [report, ...state.archive] })) },
  dismissReport: () => set({ report: undefined, state: 'IDLE' }),
}), { name: 'buildsure-emergency-state' }))

let eventsBound = false
export function bindEmergencySocketEvents() { if (eventsBound) return; eventsBound = true; listenForEmergencyEvents(session => useEmergencyStore.setState({ state: 'ACTIVE', session }), report => useEmergencyStore.setState(state => ({ state: 'CLOSED', report, session: undefined, archive: [report, ...state.archive] }))) }