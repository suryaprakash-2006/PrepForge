import { useState, useEffect } from 'react'
import { getHealth } from './services/api'
import './index.css'

function App() {
  const [healthInfo, setHealthInfo] = useState(null)
  const [loading, setLoading] = useState(true)

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

    return () => {
      mounted = false;
    }
  }, [])

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '20px', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
      <h1 style={{ borderBottom: '2px solid #eaeaea', paddingBottom: '10px' }}>PrepForge</h1>
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

export default App
