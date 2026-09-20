import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getTasks } from '../services/api';
import { Link } from 'react-router-dom';

const Dashboard = () => {
    const { user } = useAuth();
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        let mounted = true;
        const fetchTasks = async () => {
            try {
                const token = localStorage.getItem('token');
                const data = await getTasks(token);
                if (mounted) setTasks(data);
            } catch (err) {
                if (mounted) setError(err.message || 'Failed to load tasks');
            } finally {
                if (mounted) setLoading(false);
            }
        };
        fetchTasks();
        return () => { mounted = false; };
    }, []);

    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(t => t.completed).length;
    const progress = totalTasks === 0 ? 0 : Math.round((completedTasks / totalTasks) * 100);

    return (
        <div>
            <h2 style={{ borderBottom: '1px solid #eaeaea', paddingBottom: '10px' }}>Dashboard</h2>
            
            <div style={{ padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid #dee2e6', marginBottom: '20px' }}>
                <h3 style={{ marginTop: 0 }}>Overall Progress</h3>
                {loading ? (
                    <p>Loading...</p>
                ) : error ? (
                    <p style={{ color: 'red' }}>{error}</p>
                ) : totalTasks === 0 ? (
                    <p>No tasks available yet. Check your <Link to="/app/roadmap">Roadmap</Link>.</p>
                ) : (
                    <>
                        <p>Tasks completed: {completedTasks} / {totalTasks}</p>
                        <div style={{ width: '100%', backgroundColor: '#e9ecef', borderRadius: '4px', height: '20px', overflow: 'hidden' }}>
                            <div style={{ width: `${progress}%`, backgroundColor: '#28a745', height: '100%', transition: 'width 0.3s ease' }}></div>
                        </div>
                        <p style={{ textAlign: 'right', fontWeight: 'bold', margin: '5px 0 0 0' }}>{progress}%</p>
                    </>
                )}
            </div>
            
            <div style={{ padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid #dee2e6' }}>
                <h3 style={{ marginTop: 0 }}>Welcome, {user?.name}</h3>
                <p>Ready to continue your preparation?</p>
                <Link to="/app/roadmap" style={{ display: 'inline-block', padding: '10px 20px', backgroundColor: '#0066cc', color: 'white', textDecoration: 'none', borderRadius: '4px' }}>
                    View Roadmap
                </Link>
            </div>
        </div>
    );
};

export default Dashboard;
