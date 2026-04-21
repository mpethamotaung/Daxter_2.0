import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { AlertTriangle, Info, XCircle, Check } from 'lucide-react'

const severityConfig = {
  critical: { icon: XCircle, color: 'text-red-400', bg: 'bg-red-400/10', border: 'border-red-500/30' },
  warning: { icon: AlertTriangle, color: 'text-amber-400', bg: 'bg-amber-400/10', border: 'border-amber-500/30' },
  info: { icon: Info, color: 'text-blue-400', bg: 'bg-blue-400/10', border: 'border-blue-500/30' },
}

export default function AlertsPanel() {
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    const load = () => api.getAlerts(30).then(setAlerts).catch(() => {})
    load()
    const id = setInterval(load, 10000)
    return () => clearInterval(id)
  }, [])

  const handleAck = async (id) => {
    await api.acknowledgeAlert(id)
    setAlerts((prev) => prev.map((a) => a.id === id ? { ...a, acknowledged: true } : a))
  }

  const unacked = alerts.filter((a) => !a.acknowledged)
  const acked = alerts.filter((a) => a.acknowledged)

  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-gray-300">Alerts & Notifications</h3>
        {unacked.length > 0 && (
          <span className="px-2 py-0.5 text-xs font-medium bg-red-500/20 text-red-400 rounded-full">
            {unacked.length} active
          </span>
        )}
      </div>
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {unacked.length === 0 && acked.length === 0 && (
          <div className="text-gray-500 text-sm text-center py-4">No alerts yet</div>
        )}
        {unacked.map((a) => {
          const cfg = severityConfig[a.severity] || severityConfig.info
          const Icon = cfg.icon
          return (
            <div key={a.id} className={`flex items-start gap-3 p-3 rounded-lg border ${cfg.border} ${cfg.bg}`}>
              <Icon className={`w-4 h-4 mt-0.5 flex-shrink-0 ${cfg.color}`} />
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium">{a.title}</div>
                <div className="text-xs text-gray-400 mt-0.5">{a.message}</div>
                <div className="text-xs text-gray-600 mt-1">{a.source_agent} &middot; {new Date(a.created_at).toLocaleString()}</div>
              </div>
              <button onClick={() => handleAck(a.id)} className="p-1 rounded hover:bg-white/10 transition-colors"
                title="Acknowledge">
                <Check className="w-4 h-4 text-gray-400" />
              </button>
            </div>
          )
        })}
        {acked.length > 0 && (
          <>
            <div className="text-xs text-gray-600 uppercase tracking-wider pt-2">Acknowledged</div>
            {acked.slice(0, 5).map((a) => (
              <div key={a.id} className="flex items-start gap-3 p-2 rounded-lg opacity-50">
                <Check className="w-3.5 h-3.5 mt-0.5 text-gray-600" />
                <div className="text-xs text-gray-500 truncate">{a.title}</div>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  )
}
