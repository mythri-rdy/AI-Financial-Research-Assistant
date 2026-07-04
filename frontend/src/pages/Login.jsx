import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    try {
      const body = new URLSearchParams()
      body.append('username', email)
      body.append('password', password)

      const response = await api.post('/auth/login', body)
      login(response.data.access_token)
      navigate('/dashboard')
    } catch (err) {
      setError('Invalid email or password')
    }
  }
  return (
    <div className="max-w-sm mx-auto mt-20 bg-white p-8 rounded-xl shadow-sm border border-slate-200">
      <h1 className="text-xl font-semibold mb-6">Log in</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border border-slate-300 rounded-md px-3 py-2"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border border-slate-300 rounded-md px-3 py-2"
          required
        />
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button type="submit" className="bg-slate-900 text-white rounded-md py-2 hover:bg-slate-700">
          Log in
        </button>
      </form>
      <p className="text-sm text-slate-500 mt-4">
        No account? <Link to="/register" className="underline">Sign up</Link>
      </p>
    </div>
  )
}
