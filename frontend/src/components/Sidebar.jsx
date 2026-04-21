import { LayoutDashboard, FileText, Bot, MessageSquare, Bell, Activity } from 'lucide-react'

const NAV = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'tax', label: 'Tax Compliance', icon: FileText },
  { id: 'agents', label: 'Agents', icon: Bot },
  { id: 'alerts', label: 'Alerts', icon: Bell },
  { id: 'query', label: 'AI Assistant', icon: MessageSquare },
]

export default function Sidebar({ active, onNav, connected }) {
  return (
    <aside className="w-56 flex-shrink-0 bg-gray-900/70 border-r border-gray-800 flex flex-col">
      <div className="p-5 border-b border-gray-800">
        <div className="flex items-center gap-2">
          <Activity className="w-6 h-6 text-purple-400" />
          <div>
            <h1 className="text-lg font-bold tracking-tight">Daxter 2.0</h1>
            <p className="text-[10px] text-gray-500 uppercase tracking-widest">Accountant Dashboard</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-1">
        {NAV.map(({ id, label, icon: Icon }) => (
          <button key={id} onClick={() => onNav(id)}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
              active === id
                ? 'bg-purple-600/20 text-purple-300 font-medium'
                : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'
            }`}>
            <Icon className="w-4 h-4" />
            {label}
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center gap-2 text-xs">
          <span className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400' : 'bg-red-400'}`} />
          <span className="text-gray-500">{connected ? 'Live connected' : 'Reconnecting...'}</span>
        </div>
      </div>
    </aside>
  )
}
