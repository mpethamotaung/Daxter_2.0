const BASE = '/api'

async function get(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`)
  return res.json()
}

async function post(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`POST ${path} failed: ${res.status}`)
  return res.json()
}

export const api = {
  getDashboardSummary: () => get('/dashboard/summary'),
  getAgentStatuses: () => get('/agents/status'),
  getAgentLogs: (limit = 30) => get(`/agents/logs?limit=${limit}`),
  getAlerts: (limit = 30) => get(`/agents/alerts?limit=${limit}`),
  acknowledgeAlert: (id) => post(`/agents/alerts/${id}/acknowledge`, {}),
  askQuestion: (question) => post('/query/', { question }),
  getQueryHistory: () => get('/query/history'),
  getFinancialRecords: (limit = 50) => get(`/data/financial?limit=${limit}`),
  getTaxCompliance: () => get('/data/tax-compliance'),
  getReceivables: () => get('/data/receivables'),
  getPayables: () => get('/data/payables'),
  getHealth: () => get('/health'),
}
