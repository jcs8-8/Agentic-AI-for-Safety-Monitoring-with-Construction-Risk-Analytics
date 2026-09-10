import { io } from 'socket.io-client'

const socketUrl = import.meta.env.VITE_WS_URL || 'http://localhost:8000'

export const socket = io(socketUrl, {
  autoConnect: true,
  transports: ['websocket', 'polling'],
})
