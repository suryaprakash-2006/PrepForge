import React, { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom'
import { getHealth } from './services/api'
import { AuthProvider, useAuth } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Register from './pages/Register'
import AppShell from './pages/AppShell'
import Dashboard from './pages/Dashboard'
import Roadmap from './pages/Roadmap'
import Weaknesses from './pages/Weaknesses'
import WeeklyReview from './pages/WeeklyReview'
import './index.css'


const Landing = () => {
  const [healthInfo, setHealthInfo] = useState(null)
  const [loading, setLoading] = useState(true)
  const { authenticated } = useAuth()

  useEffect(() => {
    let mounted = true;
    const checkHealth = async () => {
      const data = await getHealth()
      if (mounted) {
        setHealthInfo(data)
        setLoading(false)
      }
    }
    checkHealth()
    return () => { mounted = false; }
  }, [])

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '20px', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid #eaeaea', paddingBottom: '10px' }}>
        <h1 style={{ margin: 0 }}>PrepForge</h1>
        <div>
          {authenticated ? (
            <Link to="/app" style={{ padding: '8px 16px', backgroundColor: '#0066cc', color: 'white', textDecoration: 'none', borderRadius: '4px' }}>Go to App</Link>
          ) : (
            <>
              <Link to="/login" style={{ padding: '8px 16px', color: '#0066cc', textDecoration: 'none', marginRight: '10px', border: '1px solid #0066cc', borderRadius: '4px' }}>Login</Link>
              <Link to="/register" style={{ padding: '8px 16px', backgroundColor: '#0066cc', color: 'white', textDecoration: 'none', borderRadius: '4px' }}>Register</Link>
            </>
          )}
        </div>
      </div>
      <h2>Internship Preparation & Progress Tracker</h2>
      
      <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#fafafa', borderRadius: '4px', border: '1px solid #ddd' }}>
        <h3 style={{ marginTop: 0 }}>System Status</h3>
        <p><strong>Frontend:</strong> <span style={{ color: 'green' }}>Running</span></p>
        
        {loading ? (
          <p><strong>Backend API:</strong> <span>Loading...</span></p>
        ) : healthInfo && healthInfo.status === 'ok' ? (
          <>
            <p><strong>Backend API:</strong> <span style={{ color: 'green' }}>Connected</span> (Environment: {healthInfo.environment})</p>
            <p>
              <strong>Database:</strong>{' '}
              <span style={{ color: healthInfo.database === 'connected' ? 'green' : 'red' }}>
                {healthInfo.database === 'connected' ? 'Connected' : 'Unavailable'}
              </span>
            </p>
          </>
        ) : (
          <p><strong>Backend API:</strong> <span style={{ color: 'red' }}>Unavailable</span></p>
        )}
      </div>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/app" element={<ProtectedRoute><AppShell /></ProtectedRoute>}>
            <Route index element={<Navigate to="/app/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="roadmap" element={<Roadmap />} />
            <Route path="weaknesses" element={<Weaknesses />} />
            <Route path="weekly-review" element={<WeeklyReview />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App

