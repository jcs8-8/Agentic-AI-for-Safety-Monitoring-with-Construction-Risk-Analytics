interface Props {
  agents: Array<{ agent: string; metric: string; value: number; color: string }>
}

export default function AgentPerformanceBar({ agents }: Props) {
  return (
    <div className="card">
      <h3 className="font-bold text-slate-800 mb-4 text-sm">Agent Performance Overview</h3>
      <div className="space-y-3">
        {agents.map((a, i) => (
          <div key={i}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-slate-600">{a.agent}</span>
              <span className="text-slate-800 font-medium">{a.value}% {a.metric}</span>
            </div>
            <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full rounded-full transition-all duration-700" style={{ width: `${a.value}%`, backgroundColor: a.color }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}