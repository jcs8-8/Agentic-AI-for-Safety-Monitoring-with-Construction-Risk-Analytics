import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { FileText, Download } from 'lucide-react'

export default function Reports() {
  const [reports, setReports] = useState<any[]>([])

  useEffect(() => {
    api.get('/projects/a1b2c3d4-e5f6-7890-abcd-ef1234567890/reports').then(r => setReports(r.data.data))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Reports</h2>
      <div className="grid grid-cols-1 gap-4">
        {reports.map((report) => (
          <div key={report.id} className="card flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                <FileText className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="font-bold text-slate-800">{report.type.replace(/_/g, ' ').replace(/\b\w/g, (letter: string) => letter.toUpperCase())}</p>
                <p className="text-sm text-slate-500">{report.format.toUpperCase()} • Generated {new Date(report.generated).toLocaleDateString()}</p>
              </div>
            </div>
            <button className="flex items-center gap-2 px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-200 transition">
              <Download className="w-4 h-4" /> Download
            </button>
          </div>
        ))}
        {reports.length === 0 && <p className="text-slate-500 text-center py-8">No reports generated yet.</p>}
      </div>
    </div>
  )
}