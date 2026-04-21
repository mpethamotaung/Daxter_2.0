import { useState, useRef, useEffect } from 'react'
import { api } from '../api/client'
import { Send, Bot, User, Sparkles } from 'lucide-react'

const SUGGESTIONS = [
  'Give me a financial summary',
  'What are our outstanding receivables?',
  'Show tax compliance status',
  'What are our top clients?',
  'Any active alerts?',
]

export default function QueryPanel() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async (question) => {
    const q = question || input.trim()
    if (!q) return
    setInput('')
    setMessages((prev) => [...prev, { role: 'user', text: q }])
    setLoading(true)
    try {
      const res = await api.askQuestion(q)
      setMessages((prev) => [...prev, { role: 'assistant', text: res.answer }])
    } catch {
      setMessages((prev) => [...prev, { role: 'assistant', text: 'Sorry, something went wrong. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-5 flex flex-col">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-4 h-4 text-purple-400" />
        <h3 className="text-sm font-semibold text-gray-300">AI Financial Assistant</h3>
      </div>

      {messages.length === 0 && (
        <div className="mb-4">
          <p className="text-xs text-gray-500 mb-2">Try asking:</p>
          <div className="flex flex-wrap gap-2">
            {SUGGESTIONS.map((s) => (
              <button key={s} onClick={() => send(s)}
                className="text-xs px-3 py-1.5 rounded-full bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200 transition-colors">
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="flex-1 min-h-0 max-h-80 overflow-y-auto space-y-3 mb-4">
        {messages.map((m, i) => (
          <div key={i} className={`flex gap-2 ${m.role === 'user' ? 'justify-end' : ''}`}>
            {m.role === 'assistant' && (
              <div className="p-1.5 rounded bg-purple-500/10 h-fit">
                <Bot className="w-3.5 h-3.5 text-purple-400" />
              </div>
            )}
            <div className={`max-w-[80%] p-3 rounded-xl text-sm whitespace-pre-wrap ${
              m.role === 'user'
                ? 'bg-blue-600/20 text-blue-100'
                : 'bg-gray-800/50 text-gray-300'
            }`}>
              {m.text}
            </div>
            {m.role === 'user' && (
              <div className="p-1.5 rounded bg-blue-500/10 h-fit">
                <User className="w-3.5 h-3.5 text-blue-400" />
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex gap-2">
            <div className="p-1.5 rounded bg-purple-500/10">
              <Bot className="w-3.5 h-3.5 text-purple-400 animate-pulse" />
            </div>
            <div className="bg-gray-800/50 p-3 rounded-xl text-sm text-gray-500">Analyzing...</div>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      <div className="flex gap-2">
        <input value={input} onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
          placeholder="Ask about your financial data..."
          className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-purple-500/50"
          disabled={loading}
        />
        <button onClick={() => send()} disabled={loading || !input.trim()}
          className="p-2 rounded-lg bg-purple-600 hover:bg-purple-500 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}
