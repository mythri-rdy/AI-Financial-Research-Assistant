import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()
  const handleLogout = () => {
    logout()
    navigate('/login')
  }
  return (
    <nav className="flex items-center justify-between px-6 py-4 bg-white border-b border-slate-200">
      <Link to="/" className="font-semibold text-lg text-slate-800">
        📊 AI Financial Assistant
      </Link>
      <div className="flex gap-4 items-center">
        {isAuthenticated ? (
          <button
            onClick={handleLogout}
            className="text-sm text-slate-600 hover:text-slate-900"
          >
            Log out
          </button>
        ) : (
          <>
            <Link to="/login" className="text-sm text-slate-600 hover:text-slate-900">Log in</Link>
            <Link to="/register" className="text-sm bg-slate-900 text-white px-3 py-1.5 rounded-md hover:bg-slate-700">
              Sign up
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}
