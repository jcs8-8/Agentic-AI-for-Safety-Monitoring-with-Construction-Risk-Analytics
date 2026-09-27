import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { executeCopilotAction, sendCopilotMessage } from './copilotService'
import type { CopilotAction, CopilotMessage } from './tools'

interface CopilotState {
  open: boolean
  messages: CopilotMessage[]
  busy: boolean
  activeTool?: string
  toggle: () => void
  close: () => void
  newConversation: () => void
  send: (text: string) => Promise<void>
  confirm: (action: CopilotAction) => Promise<void>
}

const message = (role: CopilotMessage['role'], text: string, extra: Partial<CopilotMessage> = {}): CopilotMessage => ({ id: `${Date.now()}-${Math.random()}`, role, text, createdAt: new Date().toISOString(), ...extra })

export const useCopilotStore = create<CopilotState>()(persist((set, get) => ({
  open: false,
  messages: [message('assistant', 'I’m your BuildSure copilot. Ask me about alerts, risk, trends, forecasts, reports, or workflows.')],
  busy: false,
  toggle: () => set(state => ({ open: !state.open })),
  close: () => set({ open: false }),
  newConversation: () => set({ messages: [message('assistant', 'New conversation started. What would you like to investigate?')] }),
  send: async (text) => {
    if (!text.trim() || get().busy) return
    set(state => ({ messages: [...state.messages, message('user', text), message('assistant', '', { status: 'pending' })], busy: true, activeTool: 'Routing to platform agents…' }))
    try {
      const response = await sendCopilotMessage(text, get().messages)
      set(state => ({ messages: state.messages.map((item, index) => index === state.messages.length - 1 ? message('assistant', response.text, { ...response, status: 'complete' }) : item), busy: false, activeTool: undefined }))
    } catch {
      set(state => ({ messages: state.messages.map((item, index) => index === state.messages.length - 1 ? message('assistant', 'I could not reach the copilot service. No platform data was changed.', { status: 'error' }) : item), busy: false, activeTool: undefined }))
    }
  },
  confirm: async (action) => {
    set({ busy: true, activeTool: 'Updating Alert Management…' })
    const response = await executeCopilotAction(action)
    set(state => ({ messages: [...state.messages, message('assistant', response.text, { tool: response.tool, source: response.source, asOf: response.asOf })], busy: false, activeTool: undefined }))
  },
}), { name: 'buildsure-copilot-conversation' }))