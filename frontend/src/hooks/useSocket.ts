import { useEffect, useRef } from 'react'
import { socket } from '@/lib/socket'

export function useSocket(projectId: string, onUpdate: () => void, onAlert?: () => void) {
  const updateRef = useRef(onUpdate)
  const alertRef = useRef(onAlert)
  updateRef.current = onUpdate
  alertRef.current = onAlert

  useEffect(() => {
    if (!projectId) return

    const updateEvent = `dashboard_update:${projectId}`
    const alertEvent = `new_alert:${projectId}`
    socket.emit('join_project', projectId)
    const handleUpdate = () => updateRef.current()
    const handleAlert = () => alertRef.current?.()
    socket.on(updateEvent, handleUpdate)
    if (onAlert) socket.on(alertEvent, handleAlert)

    return () => {
      socket.emit('leave_project', projectId)
      socket.off(updateEvent, handleUpdate)
      if (onAlert) socket.off(alertEvent, handleAlert)
    }
  }, [projectId])
}
