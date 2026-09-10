interface Props { value: number; label: string; size?: number }

export default function CircularGauge({ value, label, size = 120 }: Props) {
  const radius = (size - 16) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (value / 100) * circumference
  const color = value > 90 ? '#22c55e' : value > 75 ? '#3b82f6' : value > 60 ? '#f59e0b' : '#ef4444'

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} className="transform -rotate-90">
        <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke="#e2e8f0" strokeWidth={10} />
        <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke={color} strokeWidth={10}
          strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 1s ease' }} />
      </svg>
      <div className="text-center -mt-16 mb-4">
        <p className="text-2xl font-bold" style={{ color }}>{value}%</p>
        <p className="text-xs text-slate-500">{label}</p>
      </div>
    </div>
  )
}