import { useState, useEffect } from 'react'
import { api } from '../api/client'
import { Bot, Loader2, AlertCircle, Pause } from 'lucide-react'

const stateConfig = {
  running: { icon: Loader2, color: 'text-blue-400', bg: 'bg-blue-400/10', animate: 'animate-spin' },
  idle: { icon: Bot, color: 'text-green-400', bg: 'bg-green-400/10', animate: '' },
  error: { icon: AlertCircle, color: 'text-red-400', bg: 'bg-red-400/10', animate: '' },
  stopped: { icon: Pause, color: 'text-gray-400', bg: 'bg-gray-400/10', animate: '' },
}

export default function AgentStatus() {
  const [agents, setAgents] = useState([])
  const [logs, setLogs] = useState([])

  useEffect(() => {
    const load = () => {
      api.getAgentStatuses().then(setAgents).catch(() => {})
      api.getAgentLogs(20).then(setLogs).catch(() => {})
    }
    load()
    const id = setInterval(load, 5000)
    return () => clearInterval(id)
  }, [])

  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-5">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">Agent Orchestration</h3>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 mb-5">
        {agents.map((a) => {
          const cfg = stateConfig[a.state] || stateConfig.idle
          const Icon = cfg.icon
          return (
            <div key={a.name} className="p-3 rounded-lg bg-gray-800/50 border border-gray-700/50">
              <div className="flex items-center gap-2 mb-2">
                <div className={`p-1.5 rounded ${cfg.bg}`}>
                  <Icon className={`w-3.5 h-3.5 ${cfg.color} ${cfg.animate}`} />
                </div>
                <span className="text-xs font-medium truncate">{a.name.replace(' Agent', '')}</span>
              </div>
              <div className="text-xs text-gray-500">
                {a.records_processed} records | {a.error_count} errors
              </div>
            </div>
          )
        })}
      </div>

      <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Recent Activity</h4>
      <div className="space-y-1 max-h-44 overflow-y-auto">
        {logs.slice(0, 10).map((log) => (
          <div key={log.id} className="flex items-center gap-2 text-xs py-1.5 px-2 rounded hover:bg-gray-800/30">
            <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${
              log.state === 'error' ? 'bg-red-400' : 'bg-green-400'
            }`} />
            <span className="text-gray-400 flex-shrink-0">{new Date(log.timestamp).toLocaleTimeString()}</span>
            <span className="text-gray-300 font-medium flex-shrink-0">{log.agent_name.replace(' Agent', '')}</span>
            <span className="text-gray-500 truncate">{log.message}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
