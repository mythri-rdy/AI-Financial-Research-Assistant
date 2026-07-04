import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'

export default function Dashboard() {
  const [documents, setDocuments] = useState([])
  const [uploading, setUploading] = useState(false)

  const fetchDocuments = async () => {
    const response = await api.get('/documents/')
    setDocuments(response.data)
  }

  useEffect(() => {
    fetchDocuments()
    // Poll every 5 seconds so "processing" documents flip to "ready"
    // on the screen without the user refreshing the page manually.
    const interval = setInterval(fetchDocuments, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    setUploading(true)
    try {
      await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      await fetchDocuments()
    } finally {
      setUploading(false)
      e.target.value = ''
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 px-4">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-semibold">Your documents</h1>
        <label className="bg-slate-900 text-white text-sm px-4 py-2 rounded-md cursor-pointer hover:bg-slate-700">
          {uploading ? 'Uploading...' : 'Upload PDF'}
          <input type="file" accept="application/pdf" onChange={handleUpload} className="hidden" />
        </label>
      </div>

      {documents.length === 0 && (
        <p className="text-slate-500 text-sm">No documents yet. Upload a PDF to get started.</p>
      )}

      <div className="flex flex-col gap-3">
        {documents.map((doc) => (
          <div key={doc.id} className="bg-white border border-slate-200 rounded-lg p-4 flex items-center justify-between">
            <div>
              <p className="font-medium">{doc.filename}</p>
              <p className="text-xs text-slate-500">
                {new Date(doc.upload_date).toLocaleString()} · status: {doc.status}
              </p>
            </div>
            {doc.status === 'ready' ? (
              <Link
                to={`/chat/${doc.id}`}
                className="text-sm bg-slate-100 px-3 py-1.5 rounded-md hover:bg-slate-200"
              >
                Chat →
              </Link>
            ) : (
              <span className="text-xs text-amber-600">{doc.status}...</span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
