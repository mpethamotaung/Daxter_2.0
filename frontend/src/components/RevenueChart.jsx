import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts'

const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4', '#ef4444']

export function RevenueTrendChart({ data }) {
  if (!data || data.length === 0) {
    return <div className="text-gray-500 text-sm text-center py-8">Collecting revenue data...</div>
  }

  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-5">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">Revenue Trend (30 days)</h3>
      <ResponsiveContainer width="100%" height={260}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
          <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#6b7280' }}
            tickFormatter={(v) => v?.slice(5)} />
          <YAxis tick={{ fontSize: 11, fill: '#6b7280' }}
            tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
          <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: 8 }}
            formatter={(v) => [`$${Number(v).toLocaleString()}`, 'Revenue']} />
          <Area type="monotone" dataKey="amount" stroke="#10b981" fill="url(#revGrad)" strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

export function ExpenseCategoryChart({ data }) {
  if (!data || data.length === 0) {
    return <div className="text-gray-500 text-sm text-center py-8">Collecting expense data...</div>
  }

  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-5">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">Expenses by Category</h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
          <XAxis type="number" tick={{ fontSize: 11, fill: '#6b7280' }}
            tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
          <YAxis dataKey="category" type="category" width={140}
            tick={{ fontSize: 11, fill: '#6b7280' }} />
          <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: 8 }}
            formatter={(v) => [`$${Number(v).toLocaleString()}`, 'Amount']} />
          <Bar dataKey="amount" radius={[0, 4, 4, 0]}>
            {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
