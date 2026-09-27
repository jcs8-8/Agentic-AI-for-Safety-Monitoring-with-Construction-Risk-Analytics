import { api } from '@/lib/api'
import type { FrontDeskState, Ticket, TicketStatus, Visitor } from './types'

const mode = import.meta.env.VITE_FRONT_DESK_MODE || 'mock'

const initial: FrontDeskState = {
  visitors: [
    { id: 'v-1', name: 'Priya Menon', company: 'Apex Structural', host: 'Rajesh Kumar', purpose: 'Structural inspection', appointment: '09:30', status: 'Checked in', badge: 'VIS-042', checkedInAt: '09:27' },
    { id: 'v-2', name: 'Marcus Lee', company: 'BuildSure Insurance', host: 'John Doe', purpose: 'Claims review', appointment: '11:00', status: 'Expected', badge: 'VIS-043' },
    { id: 'v-3', name: 'Anita Shah', company: 'City Utilities', host: 'Safety Team', purpose: 'Gas line survey', appointment: '14:00', status: 'Expected', badge: 'VIS-044' },
  ],
  deliveries: [{ id: 'd-1', supplier: 'Metro Steel', reference: 'PO-8842', destination: 'Zone C laydown', eta: '10:30', status: 'Expected', contact: '+91 98765 11223' }, { id: 'd-2', supplier: 'SafeLift Rentals', reference: 'SL-2019', destination: 'Site office', eta: '08:45', status: 'Received', contact: '+91 98765 44556' }],
  tickets: [{ id: 'ENG-1042', title: 'Tower crane inspection light offline', category: 'Mechanical', priority: 'High', status: 'In progress', assignee: 'Arjun Patel', location: 'Crane 3', createdAt: 'Today 08:12', dueAt: 'Today 12:00', description: 'Camera and inspection light are not responding at the crane access platform.' }, { id: 'ENG-1041', title: 'Water pooling near Zone B walkway', category: 'Safety', priority: 'Critical', status: 'Open', assignee: 'Unassigned', location: 'Zone B', createdAt: 'Today 07:46', dueAt: 'Today 09:30', description: 'Clear standing water and inspect the drainage route before the next shift.' }, { id: 'ENG-1039', title: 'Temporary office printer offline', category: 'IT', priority: 'Low', status: 'Resolved', assignee: 'Nikhil Rao', location: 'Site office', createdAt: 'Yesterday 16:20', dueAt: 'Yesterday 18:00', description: 'Replace toner and reconnect the printer.' }],
  workers: [{ id: 'w-1', name: 'Rajesh Kumar', company: 'BuildRight Civil', trade: 'Site manager', zone: 'Zone B', status: 'On site', induction: 'Valid', permit: 'Valid', lastSeen: '2 min ago' }, { id: 'w-2', name: 'Sanjay Rao', company: 'Apex Electrical', trade: 'Electrician', zone: 'Zone C', status: 'On site', induction: 'Valid', permit: 'Due', lastSeen: '5 min ago' }, { id: 'w-3', name: 'Meera Das', company: 'SafeScaffold', trade: 'Scaffolder', zone: 'Zone A', status: 'Off site', induction: 'Expired', permit: 'Expired', lastSeen: 'Yesterday 18:10' }, { id: 'w-4', name: 'Owen Smith', company: 'Metro Steel', trade: 'Rigger', zone: 'Zone C', status: 'On site', induction: 'Valid', permit: 'Valid', lastSeen: '1 min ago' }], musterActive: false, attendanceLog: [],
}

export async function getFrontDesk(): Promise<FrontDeskState> { if (mode === 'live') return (await api.get('/front-desk')).data.data; return initial }
export async function saveFrontDesk(state: FrontDeskState): Promise<FrontDeskState> { if (mode === 'live') return (await api.put('/front-desk', state)).data.data; return state }
export async function createTicket(ticket: Omit<Ticket, 'id' | 'createdAt'>): Promise<Ticket> { if (mode === 'live') return (await api.post('/front-desk/tickets', ticket)).data.data; return { ...ticket, id: `ENG-${1043 + Math.floor(Math.random() * 100)}`, createdAt: `Today ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}` } }
export async function createVisitor(visitor: Omit<Visitor, 'id' | 'status' | 'badge'>): Promise<Visitor> { if (mode === 'live') return (await api.post('/front-desk/visitors', visitor)).data.data; return { ...visitor, id: `v-${Date.now()}`, status: 'Expected', badge: `VIS-${Math.floor(100 + Math.random() * 899)}` } }
export async function checkInVisitor(visitor: Visitor): Promise<Visitor> { if (mode === 'live') return (await api.post(`/front-desk/visitors/${visitor.id}/check-in`)).data.data; return { ...visitor, status: 'Checked in', checkedInAt: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) } }
export async function updateTicketStatus(id: string, status: TicketStatus, assignee: string): Promise<void> { if (mode === 'live') await api.patch(`/front-desk/tickets/${id}`, { status, assignee }) }
export { initial }