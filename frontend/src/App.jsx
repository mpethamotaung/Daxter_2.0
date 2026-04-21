import { useState, useEffect, useCallback } from 'react'
import { api } from './api/client'
import { useWebSocket } from './hooks/useWebSocket'
import Sidebar from './components/Sidebar'
import KPICards from './components/KPICards'
import { RevenueTrendChart, ExpenseCategoryChart } from './components/RevenueChart'
import TaxCompliance from './components/TaxCompliance'
import AgentStatus from './components/AgentStatus'
import AlertsPanel from './components/AlertsPanel'
import QueryPanel from './components/QueryPanel'
import { RefreshCw } from 'lucide-react'

export default function App() {
  const [view, setView] = useState('dashboard')
  const [summary, setSummary] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(null)

  const loadSummary = useCallback(() => {
    api.getDashboardSummary().then((data) => {
      setSummary(data)
      setLastUpdate(new Date())
    }).catch(() => {})
  }, [])

  const onWsMessage = useCallback((event) => {
    if (event.type === 'cycle_complete') {
      loadSummary()
    }
  }, [loadSummary])

  const connected = useWebSocket(onWsMessage)

  useEffect(() => {
    loadSummary()
  }, [loadSummary])

  return (
    <div className="h-screen flex overflow-hidden">
      <Sidebar active={view} onNav={setView} connected={connected} />

      <main className="flex-1 overflow-y-auto">
        <header className="sticky top-0 z-10 bg-gray-950/80 backdrop-blur border-b border-gray-800 px-6 py-3 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold capitalize">
              {view === 'query' ? 'AI Assistant' : view === 'tax' ? 'Tax Compliance' : view}
            </h2>
            {lastUpdate && (
              <p className="text-xs text-gray-500">
                Last updated: {lastUpdate.toLocaleTimeString()}
              </p>
            )}
          </div>
          <button onClick={loadSummary}
            className="p-2 rounded-lg hover:bg-gray-800 transition-colors text-gray-400 hover:text-gray-200"
            title="Refresh">
            <RefreshCw className="w-4 h-4" />
          </button>
        </header>

        <div className="p-6 space-y-6">
          {view === 'dashboard' && (
            <>
              <KPICards summary={summary} />
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <RevenueTrendChart data={summary?.revenue_trend} />
                <ExpenseCategoryChart data={summary?.expense_by_category} />
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <TaxCompliance />
                <AlertsPanel />
              </div>
              <AgentStatus />
              <QueryPanel />
            </>
          )}
          {view === 'tax' && <TaxCompliance />}
          {view === 'agents' && <AgentStatus />}
          {view === 'alerts' && <AlertsPanel />}
          {view === 'query' && <QueryPanel />}
        </div>
      </main>
    </div>
  )
}
