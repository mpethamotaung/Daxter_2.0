import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { ShieldCheck, ShieldAlert, Clock, ShieldX } from 'lucide-react'

const statusConfig = {
  compliant: { icon: ShieldCheck, label: 'Compliant', color: 'text-green-400 bg-green-400/10' },
  warning: { icon: Clock, label: 'Warning', color: 'text-amber-400 bg-amber-400/10' },
  non_compliant: { icon: ShieldX, label: 'Non-Compliant', color: 'text-red-400 bg-red-400/10' },
  pending: { icon: ShieldAlert, label: 'Pending', color: 'text-blue-400 bg-blue-400/10' },
}

export default function TaxCompliance() {
  const [filings, setFilings] = useState([])

  useEffect(() => {
    const load = () => api.getTaxCompliance().then(setFilings).catch(() => {})
    load()
    const id = setInterval(load, 15000)
    return () => clearInterval(id)
  }, [])

  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-5">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">Tax Compliance Tracker</h3>
      <div className="space-y-2 max-h-80 overflow-y-auto">
        {filings.length === 0 && <div className="text-gray-500 text-sm text-center py-4">Loading filings...</div>}
        {filings.slice(0, 15).map((f) => {
          const cfg = statusConfig[f.status] || statusConfig.pending
          const Icon = cfg.icon
          const deadline = new Date(f.deadline)
          const daysUntil = Math.ceil((deadline - new Date()) / 86400000)
          return (
            <div key={f.id} className="flex items-center gap-3 p-3 rounded-lg bg-gray-800/50 hover:bg-gray-800 transition-colors">
              <div className={`p-2 rounded-lg ${cfg.color}`}>
                <Icon className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium truncate">{f.filing_type}</div>
                <div className="text-xs text-gray-500">{f.jurisdiction}</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium">${Number(f.amount_due).toLocaleString()}</div>
                <div className={`text-xs ${daysUntil < 0 ? 'text-red-400' : daysUntil < 14 ? 'text-amber-400' : 'text-gray-500'}`}>
                  {daysUntil < 0 ? `${Math.abs(daysUntil)}d overdue` : `${daysUntil}d left`}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
