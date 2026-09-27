export type FrontDeskTab = 'reception' | 'helpdesk' | 'site'
export type VisitorStatus = 'Expected' | 'Checked in' | 'Checked out'
export type TicketStatus = 'Open' | 'In progress' | 'Blocked' | 'Resolved'
export type WorkerStatus = 'On site' | 'Off site'

export interface Visitor { id: string; name: string; company: string; host: string; purpose: string; appointment: string; status: VisitorStatus; badge: string; checkedInAt?: string }
export interface Delivery { id: string; supplier: string; reference: string; destination: string; eta: string; status: 'Expected' | 'Received' | 'Delayed'; contact: string }
export interface Ticket { id: string; title: string; category: 'Electrical' | 'Mechanical' | 'Safety' | 'IT' | 'Other'; priority: 'Low' | 'Medium' | 'High' | 'Critical'; status: TicketStatus; assignee: string; location: string; createdAt: string; dueAt: string; description: string }
export interface Worker { id: string; name: string; company: string; trade: string; zone: string; status: WorkerStatus; induction: 'Valid' | 'Due' | 'Expired'; permit: 'Valid' | 'Due' | 'Missing' | 'Expired'; lastSeen: string }
export interface FrontDeskState { visitors: Visitor[]; deliveries: Delivery[]; tickets: Ticket[]; workers: Worker[]; musterActive: boolean; musterStartedAt?: string; attendanceLog: string[] }