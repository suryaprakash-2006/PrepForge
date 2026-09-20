import React from 'react';
import { useAuth } from '../context/AuthContext';

const AppShell = () => {
    const { user, logout } = useAuth();

    return (
        <div style={{ maxWidth: '800px', margin: '40px auto', padding: '30px', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid #eaeaea', paddingBottom: '15px', marginBottom: '20px' }}>
                <h1 style={{ margin: 0 }}>PrepForge</h1>
                <button 
                    onClick={logout}
                    style={{ padding: '8px 16px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                >
                    Logout
                </button>
            </div>
            
            <h2>Welcome, {user?.name || 'User'}</h2>
            
            <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid #dee2e6' }}>
                <h3 style={{ marginTop: 0, borderBottom: '1px solid #dee2e6', paddingBottom: '10px' }}>Profile Information</h3>
                <p><strong>Name:</strong> {user?.name}</p>
                <p><strong>Email:</strong> {user?.email}</p>
                <p><strong>Authentication status:</strong> <span style={{ color: 'green', fontWeight: 'bold' }}>Authenticated</span></p>
                
                <div style={{ marginTop: '20px', fontSize: '14px', color: '#6c757d' }}>
                    <p><em>(This is a temporary authentication verification screen. The full dashboard will be implemented in future milestones.)</em></p>
                </div>
            </div>
        </div>
    );
};

export default AppShell;
