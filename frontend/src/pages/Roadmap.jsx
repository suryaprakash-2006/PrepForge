import React, { useState, useEffect } from 'react';
import { getWeeks, initializeRoadmap, getTasks, updateTask } from '../services/api';

const Roadmap = () => {
    const [weeks, setWeeks] = useState([]);
    const [loadingWeeks, setLoadingWeeks] = useState(true);
    const [initializing, setInitializing] = useState(false);
    const [error, setError] = useState('');
    
    const [selectedWeek, setSelectedWeek] = useState(null);
    const [tasks, setTasks] = useState([]);
    const [loadingTasks, setLoadingTasks] = useState(false);
    const [updatingTask, setUpdatingTask] = useState(null);

    const fetchWeeks = async () => {
        setLoadingWeeks(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const data = await getWeeks(token);
            setWeeks(data);
        } catch (err) {
            setError(err.message || 'Failed to load weeks');
        } finally {
            setLoadingWeeks(false);
        }
    };

    useEffect(() => {
        fetchWeeks();
    }, []);

    const handleInitialize = async () => {
        setInitializing(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            await initializeRoadmap(token);
            await fetchWeeks();
        } catch (err) {
            setError(err.message || 'Failed to initialize roadmap');
        } finally {
            setInitializing(false);
        }
    };

    const handleSelectWeek = async (week) => {
        setSelectedWeek(week);
        setLoadingTasks(true);
        try {
            const token = localStorage.getItem('token');
            const data = await getTasks(token, week.id);
            setTasks(data);
        } catch (err) {
            setError(err.message || 'Failed to load tasks');
        } finally {
            setLoadingTasks(false);
        }
    };

    const handleToggleTask = async (task) => {
        setUpdatingTask(task.id);
        const originalStatus = task.completed;
        const newStatus = !originalStatus;
        
        // Optimistic update locally
        setTasks(tasks.map(t => t.id === task.id ? { ...t, completed: newStatus } : t));
        
        try {
            const token = localStorage.getItem('token');
            const updated = await updateTask(token, task.id, { completed: newStatus });
            // Sync with backend confirmed state
            setTasks(tasks.map(t => t.id === task.id ? updated : t));
        } catch (err) {
            // Revert on failure
            setTasks(tasks.map(t => t.id === task.id ? { ...t, completed: originalStatus } : t));
            setError(err.message || 'Failed to update task');
        } finally {
            setUpdatingTask(null);
        }
    };

    if (loadingWeeks) {
        return <div>Loading roadmap...</div>;
    }

    if (weeks.length === 0) {
        return (
            <div>
                <h2 style={{ borderBottom: '1px solid #eaeaea', paddingBottom: '10px' }}>12-Week Roadmap</h2>
                {error && <div style={{ color: 'red', marginBottom: '15px' }}>{error}</div>}
                
                <div style={{ padding: '30px', textAlign: 'center', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid #dee2e6' }}>
                    <h3>Your 12-week roadmap hasn't been initialized yet.</h3>
                    <p style={{ color: '#666', marginBottom: '20px' }}>Set up your default study plan to get started.</p>
                    <button 
                        onClick={handleInitialize}
                        disabled={initializing}
                        style={{ padding: '12px 24px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '4px', cursor: initializing ? 'not-allowed' : 'pointer', fontSize: '16px' }}
                    >
                        {initializing ? 'Initializing...' : 'Initialize Roadmap'}
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div>
            <h2 style={{ borderBottom: '1px solid #eaeaea', paddingBottom: '10px' }}>12-Week Roadmap</h2>
            {error && <div style={{ backgroundColor: '#fee', color: 'red', padding: '10px', borderRadius: '4px', marginBottom: '15px', border: '1px solid #fcc' }}>{error}</div>}
            
            <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
                <div style={{ flex: '1', minWidth: '250px' }}>
                    <h3 style={{ marginTop: 0 }}>Weeks</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        {weeks.map(week => (
                            <div 
                                key={week.id} 
                                onClick={() => handleSelectWeek(week)}
                                style={{ 
                                    padding: '15px', 
                                    backgroundColor: selectedWeek?.id === week.id ? '#e6f2ff' : 'white', 
                                    border: selectedWeek?.id === week.id ? '1px solid #0066cc' : '1px solid #ddd',
                                    borderRadius: '4px',
                                    cursor: 'pointer',
                                    transition: 'background-color 0.2s'
                                }}
                            >
                                <div style={{ fontWeight: 'bold' }}>Week {week.week_number}</div>
                                <div style={{ fontSize: '14px', color: '#555' }}>{week.title}</div>
                            </div>
                        ))}
                    </div>
                </div>

                <div style={{ flex: '2', backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '4px', border: '1px solid #dee2e6', minHeight: '400px' }}>
                    {!selectedWeek ? (
                        <div style={{ textAlign: 'center', color: '#777', marginTop: '50px' }}>
                            Select a week to view its tasks.
                        </div>
                    ) : (
                        <div>
                            <h3 style={{ marginTop: 0 }}>Week {selectedWeek.week_number}: {selectedWeek.title}</h3>
                            <p style={{ color: '#555', marginBottom: '20px' }}>{selectedWeek.description}</p>
                            
                            <h4>Tasks</h4>
                            {loadingTasks ? (
                                <div>Loading tasks...</div>
                            ) : tasks.length === 0 ? (
                                <div style={{ color: '#777' }}>No tasks found for this week.</div>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                                    {tasks.map(task => (
                                        <div key={task.id} style={{ display: 'flex', alignItems: 'flex-start', gap: '15px', padding: '15px', backgroundColor: 'white', border: '1px solid #ddd', borderRadius: '4px' }}>
                                            <input 
                                                type="checkbox" 
                                                checked={task.completed}
                                                onChange={() => handleToggleTask(task)}
                                                disabled={updatingTask === task.id}
                                                style={{ marginTop: '5px', width: '18px', height: '18px', cursor: updatingTask === task.id ? 'wait' : 'pointer' }}
                                            />
                                            <div style={{ flex: 1 }}>
                                                <div style={{ fontWeight: 'bold', textDecoration: task.completed ? 'line-through' : 'none', color: task.completed ? '#888' : '#000' }}>
                                                    {task.title}
                                                </div>
                                                {task.description && <div style={{ fontSize: '14px', color: '#555', marginTop: '5px' }}>{task.description}</div>}
                                                <div style={{ fontSize: '12px', color: '#888', marginTop: '8px', display: 'flex', gap: '15px' }}>
                                                    {task.category && <span>Category: {task.category}</span>}
                                                    {task.estimated_minutes && <span>Est: {task.estimated_minutes}m</span>}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Roadmap;
