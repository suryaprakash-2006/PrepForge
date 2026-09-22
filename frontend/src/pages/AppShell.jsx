import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Outlet, Link, useLocation } from 'react-router-dom';

const AppShell = () => {
    const { logout } = useAuth();
    const location = useLocation();

    return (
        <div style={{ maxWidth: '900px', margin: '40px auto', padding: '30px', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid #eaeaea', paddingBottom: '15px', marginBottom: '20px' }}>
                <h1 style={{ margin: 0 }}>PrepForge</h1>
                <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                    <Link 
                        to="/app/dashboard" 
                        style={{ color: location.pathname === '/app/dashboard' ? '#0066cc' : '#555', textDecoration: 'none', fontWeight: location.pathname === '/app/dashboard' ? 'bold' : 'normal' }}
                    >
                        Dashboard
                    </Link>
                    <Link 
                        to="/app/roadmap" 
                        style={{ color: location.pathname === '/app/roadmap' ? '#0066cc' : '#555', textDecoration: 'none', fontWeight: location.pathname === '/app/roadmap' ? 'bold' : 'normal' }}
                    >
                        Roadmap
                    </Link>
                    <Link 
                        to="/app/weaknesses" 
                        style={{ color: location.pathname === '/app/weaknesses' ? '#0066cc' : '#555', textDecoration: 'none', fontWeight: location.pathname === '/app/weaknesses' ? 'bold' : 'normal' }}
                    >
                        Weaknesses
                    </Link>
                    <Link 
                        to="/app/weekly-review" 
                        style={{ color: location.pathname === '/app/weekly-review' ? '#0066cc' : '#555', textDecoration: 'none', fontWeight: location.pathname === '/app/weekly-review' ? 'bold' : 'normal' }}
                    >
                        Weekly Review
                    </Link>
                    <Link 
                        to="/app/assessments" 
                        style={{ color: location.pathname === '/app/assessments' ? '#0066cc' : '#555', textDecoration: 'none', fontWeight: location.pathname === '/app/assessments' ? 'bold' : 'normal' }}
                    >
                        Assessments
                    </Link>
                    <button 
                        onClick={logout}
                        style={{ padding: '6px 12px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginLeft: '10px' }}
                    >
                        Logout
                    </button>
                </div>
            </div>
            
            <Outlet />
        </div>
    );
};

export default AppShell;
