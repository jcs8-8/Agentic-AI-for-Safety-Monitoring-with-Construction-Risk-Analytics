import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { checkInVisitor, createTicket, createVisitor, getFrontDesk, initial, saveFrontDesk, updateTicketStatus } from './frontDeskService'
import type { FrontDeskState, Ticket, TicketStatus, Visitor } from './types'

interface Store extends FrontDeskState { hydrated: boolean; load: () => Promise<void>; registerVisitor: (visitor: Omit<Visitor, 'id' | 'status' | 'badge'>) => Promise<void>; checkIn: (id: string) => Promise<void>; addTicket: (ticket: Omit<Ticket, 'id' | 'createdAt'>) => Promise<void>; updateTicket: (id: string, status: TicketStatus, assignee: string) => Promise<void>; toggleMuster: () => Promise<void>; recordAttendance: (workerId: string) => Promise<void> }

export const useFrontDeskStore = create<Store>()(persist((set, get) => ({ ...initial, hydrated: false,
  load: async () => { const state = await getFrontDesk(); set({ ...state, hydrated: true }) },
  registerVisitor: async visitor => { const created = await createVisitor(visitor); const state = { ...get(), visitors: [...get().visitors, created] }; set(state); await saveFrontDesk(state) },
  checkIn: async id => { const visitor = get().visitors.find(item => item.id === id); if (!visitor) return; const updated = await checkInVisitor(visitor); const state = { ...get(), visitors: get().visitors.map(item => item.id === id ? updated : item) }; set(state); await saveFrontDesk(state) },
  addTicket: async ticket => { const created = await createTicket(ticket); const state = { ...get(), tickets: [created, ...get().tickets] }; set(state); await saveFrontDesk(state) },
  updateTicket: async (id, status, assignee) => { const state = { ...get(), tickets: get().tickets.map(ticket => ticket.id === id ? { ...ticket, status, assignee } : ticket) }; set(state); await updateTicketStatus(id, status, assignee); await saveFrontDesk(state) },
  toggleMuster: async () => { const active = !get().musterActive; const state = { ...get(), musterActive: active, musterStartedAt: active ? new Date().toISOString() : undefined }; set(state); await saveFrontDesk(state) },
  recordAttendance: async workerId => { const state = { ...get(), attendanceLog: [...get().attendanceLog, `${workerId}:${new Date().toISOString()}`] }; set(state); await saveFrontDesk(state) },
}), { name: 'buildsure-front-desk-state' }))