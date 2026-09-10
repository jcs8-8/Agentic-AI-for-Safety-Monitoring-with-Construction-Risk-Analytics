import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { Play, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

interface Agent { agent_name: string; status: string; last_run: string | null; findings_count: number; is_running: boolean }

export default function AgentOrchestrator() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadAgents()
  }, [])

  const loadAgents = () => {
    api.get('/agents').then(r => setAgents(r.data.data))
  }

  const triggerAgent = async (name: string) => {
    setLoading(true)
    await api.post(`/agents/${name}/trigger`, { project_id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890' })
    loadAgents()
    setLoading(false)
  }

  const orchestrateAll = async () => {
    setLoading(true)
    await api.post('/agents/orchestrate', { project_id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890' })
    loadAgents()
    setLoading(false)
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-slate-800">Agent Orchestrator</h2>
        <button onClick={orchestrateAll} disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-accent-orange text-white rounded-lg font-medium hover:bg-orange-600 transition disabled:opacity-50">
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
          Run All Agents
        </button>
      </div>
      <div className="grid grid-cols-1 gap-4">
        {agents.map((agent) => (
          <div key={agent.agent_name} className="card flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                agent.status === 'completed' ? 'bg-green-100' : agent.status === 'running' ? 'bg-yellow-100' : 'bg-slate-100'
              }`}>
                {agent.status === 'completed' ? <CheckCircle className="w-5 h-5 text-green-600" /> :
                 agent.status === 'running' ? <Loader2 className="w-5 h-5 text-yellow-600 animate-spin" /> :
                 <AlertCircle className="w-5 h-5 text-slate-500" />}
              </div>
              <div>
                <p className="font-bold text-slate-800">{agent.agent_name}</p>
                <p className="text-sm text-slate-500">Status: {agent.status} | Findings: {agent.findings_count}</p>
              </div>
            </div>
            <button onClick={() => triggerAgent(agent.agent_name)} disabled={loading || agent.is_running}
              className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-200 transition disabled:opacity-50">
              {agent.is_running ? 'Running...' : 'Trigger'}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}