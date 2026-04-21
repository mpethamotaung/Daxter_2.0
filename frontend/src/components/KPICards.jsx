import { DollarSign, TrendingUp, TrendingDown, FileText, AlertTriangle, Bot, Receipt, CreditCard } from 'lucide-react'

function Card({ title, value, icon: Icon, color, subtitle }) {
  const colors = {
    green: 'from-green-500/20 to-green-900/10 border-green-500/30',
    red: 'from-red-500/20 to-red-900/10 border-red-500/30',
    blue: 'from-blue-500/20 to-blue-900/10 border-blue-500/30',
    amber: 'from-amber-500/20 to-amber-900/10 border-amber-500/30',
    purple: 'from-purple-500/20 to-purple-900/10 border-purple-500/30',
    cyan: 'from-cyan-500/20 to-cyan-900/10 border-cyan-500/30',
  }

  const iconColors = {
    green: 'text-green-400',
    red: 'text-red-400',
    blue: 'text-blue-400',
    amber: 'text-amber-400',
    purple: 'text-purple-400',
    cyan: 'text-cyan-400',
  }

  return (
    <div className={`bg-gradient-to-br ${colors[color]} border rounded-xl p-5`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-gray-400 font-medium">{title}</span>
        <Icon className={`w-5 h-5 ${iconColors[color]}`} />
      </div>
      <div className="text-2xl font-bold tracking-tight">{value}</div>
      {subtitle && <div className="text-xs text-gray-500 mt-1">{subtitle}</div>}
    </div>
  )
}

export default function KPICards({ summary }) {
  if (!summary) return null

  const fmt = (n) => `$${Number(n).toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <Card title="Total Revenue" value={fmt(summary.total_revenue)} icon={TrendingUp} color="green" />
      <Card title="Total Expenses" value={fmt(summary.total_expenses)} icon={TrendingDown} color="red" />
      <Card title="Net Income" value={fmt(summary.net_income)} icon={DollarSign}
        color={summary.net_income >= 0 ? 'green' : 'red'} />
      <Card title="Outstanding AR" value={fmt(summary.outstanding_receivables)} icon={Receipt} color="blue" />
      <Card title="Outstanding AP" value={fmt(summary.outstanding_payables)} icon={CreditCard} color="purple" />
      <Card title="Tax Deadlines" value={summary.upcoming_tax_deadlines}
        icon={FileText} color="amber" subtitle="Within 30 days" />
      <Card title="Compliance Warnings" value={summary.compliance_warnings}
        icon={AlertTriangle} color={summary.compliance_warnings > 0 ? 'red' : 'green'} />
      <Card title="Active Agents" value={summary.active_agents} icon={Bot} color="cyan" />
    </div>
  )
}
