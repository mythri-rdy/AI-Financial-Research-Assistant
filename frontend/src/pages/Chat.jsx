import { useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'

export default function Chat() {
  const { documentId } = useParams()
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([]) 
  const [loading, setLoading] = useState(false)

  const handleAsk = async (e) => {
    e.preventDefault()
    if (!question.trim()) return
    const currentQuestion = question
    setMessages((prev) => [...prev, { role: 'user', text: currentQuestion }])
    setQuestion('')
    setLoading(true)
    try {
      const response = await api.post('/chat/ask', {
        document_id: Number(documentId),
        question: currentQuestion,
      })
      setMessages((prev) => [
        ...prev,
        { role: 'ai', text: response.data.answer, sources: response.data.sources },
      ])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'ai', text: 'Something went wrong answering that. Try again.', sources: [] },
      ])
    } finally {
      setLoading(false)
    }
  }
  return (
    <div className="max-w-2xl mx-auto mt-8 px-4 flex flex-col h-[80vh]">
      <h1 className="text-lg font-semibold mb-4">Ask this document</h1>
      <div className="flex-1 overflow-y-auto flex flex-col gap-3 mb-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded-lg max-w-[80%] ${
              msg.role === 'user'
                ? 'bg-slate-900 text-white self-end'
                : 'bg-white border border-slate-200 self-start'
            }`}
          >
            <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
            {msg.sources?.length > 0 && (
              <p className="text-xs text-slate-400 mt-2">Sources: {msg.sources.join(', ')}</p>
            )}
          </div>
        ))}
        {loading && <p className="text-sm text-slate-400">Thinking...</p>}
      </div>
      <form onSubmit={handleAsk} className="flex gap-2">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What were the major business risks?"
          className="flex-1 border border-slate-300 rounded-md px-3 py-2 text-sm"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-slate-900 text-white text-sm px-4 py-2 rounded-md hover:bg-slate-700 disabled:opacity-50"
        >
          Ask
        </button>
      </form>
    </div>
  )
}
