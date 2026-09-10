import { ArrowDown, Bell, BrainCircuit, Database, FileText, Gauge, ShieldCheck, Workflow } from 'lucide-react'

const workflow = [
  { title: 'Construction Site Data', detail: 'CCTV, inspections, worker attendance, PPE, incidents', icon: Database, tone: 'blue' },
  { title: 'Data Validation & Processing', detail: 'Normalize events and prepare trusted project signals', icon: Workflow, tone: 'slate' },
  { title: 'Specialized AI Agents', detail: 'Site Risk, Safety, Compliance, Insurance, Reporting', icon: BrainCircuit, tone: 'orange' },
  { title: 'Risk Intelligence Engine', detail: 'Scores, predictions, recurring patterns, recommendations', icon: Gauge, tone: 'indigo' },
  { title: 'Project Dashboards & Alerts', detail: 'Live dashboards, reports, notifications, and actions', icon: Bell, tone: 'green' },
]

const layers = [
  ['Data Sources', 'Site inspections', 'CCTV and PPE signals', 'Incident reports', 'Compliance documents'],
  ['Intelligence', 'Safety Agent', 'Compliance Agent', 'Insurance Agent', 'Risk Intelligence Engine'],
  ['Experience', 'Safety Dashboard', 'Compliance Dashboard', 'Insurance Dashboard', 'Executive Overview'],
]

export default function Architecture() {
  return (
    <div className="space-y-8">
      <header><p className="text-sm font-semibold uppercase tracking-widest text-accent-orange">System blueprint</p><h2 className="mt-2 text-3xl font-bold text-slate-800">Architecture & Workflow</h2><p className="mt-2 max-w-3xl text-slate-500">A single flow from construction-site signals to decisions, alerts, and measurable risk reduction.</p></header>
      <section className="card">
        <div className="mb-6 flex items-center gap-3"><Workflow className="h-6 w-6 text-accent-orange" /><h3 className="text-lg font-bold text-slate-800">BuildSure AI workflow</h3></div>
        <div className="mx-auto max-w-2xl">{workflow.map((step, index) => { const Icon = step.icon; return <div key={step.title} className="flex flex-col items-center"><div className={`flex w-full items-center gap-4 rounded-xl border p-4 ${step.tone === 'orange' ? 'border-orange-200 bg-orange-50' : 'border-slate-200 bg-slate-50'}`}><div className="rounded-lg bg-white p-3 shadow-sm"><Icon className="h-5 w-5 text-accent-orange" /></div><div><h4 className="font-bold text-slate-800">{step.title}</h4><p className="mt-1 text-sm text-slate-500">{step.detail}</p></div></div>{index < workflow.length - 1 && <ArrowDown className="my-2 h-5 w-5 text-slate-400" />}</div> })}</div>
      </section>
      <section className="grid gap-5 lg:grid-cols-3">{layers.map(([title, ...items], index) => <div className="card" key={title}><div className="mb-4 flex items-center gap-2"><div className={`rounded-lg p-2 ${index === 0 ? 'bg-blue-50 text-blue-600' : index === 1 ? 'bg-orange-50 text-orange-600' : 'bg-green-50 text-green-600'}`}>{index === 0 ? <Database className="h-5 w-5" /> : index === 1 ? <ShieldCheck className="h-5 w-5" /> : <FileText className="h-5 w-5" />}</div><h3 className="font-bold text-slate-800">{title}</h3></div><div className="space-y-2">{items.map(item => <div className="rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-600" key={item}>{item}</div>)}</div></div>)}</section>
    </div>
  )
}
