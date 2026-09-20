import React, { useState, useEffect, useMemo } from 'react';
import { getWeeks, initializeRoadmap, getTasks, updateTask } from '../services/api';

const Roadmap = () => {
    const [weeks, setWeeks] = useState([]);
    const [allTasks, setAllTasks] = useState([]);
    const [loadingData, setLoadingData] = useState(true);
    const [initializing, setInitializing] = useState(false);
    const [error, setError] = useState('');
    
    const [selectedWeek, setSelectedWeek] = useState(null);
    const [updatingTask, setUpdatingTask] = useState(null);

    // Filters and Search
    const [searchQuery, setSearchQuery] = useState('');
    const [statusFilter, setStatusFilter] = useState('All');
    const [categoryFilter, setCategoryFilter] = useState('All');

    const fetchData = async () => {
        setLoadingData(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const [weeksData, tasksData] = await Promise.all([
                getWeeks(token),
                getTasks(token) // fetch all tasks without week_id
            ]);
            setWeeks(weeksData);
            setAllTasks(tasksData);
        } catch (err) {
            setError(err.message || 'Failed to load roadmap data');
        } finally {
            setLoadingData(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleInitialize = async () => {
        setInitializing(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            await initializeRoadmap(token);
            await fetchData();
        } catch (err) {
            setError(err.message || 'Failed to initialize roadmap');
        } finally {
            setInitializing(false);
        }
    };

    const handleToggleTask = async (task) => {
        setUpdatingTask(task.id);
        const originalStatus = task.completed;
        const newStatus = !originalStatus;
        
        // Optimistic update locally
        setAllTasks(allTasks.map(t => t.id === task.id ? { ...t, completed: newStatus } : t));
        
        try {
            const token = localStorage.getItem('token');
            const updated = await updateTask(token, task.id, { completed: newStatus });
            // Sync with backend confirmed state
            setAllTasks(prevTasks => prevTasks.map(t => t.id === task.id ? updated : t));
        } catch (err) {
            // Revert on failure
            setAllTasks(prevTasks => prevTasks.map(t => t.id === task.id ? { ...t, completed: originalStatus } : t));
            setError(err.message || 'Failed to update task');
        } finally {
            setUpdatingTask(null);
        }
    };

    // Derived states
    const tasksByWeek = useMemo(() => {
        const map = {};
        allTasks.forEach(t => {
            if (!map[t.week_id]) map[t.week_id] = [];
            map[t.week_id].push(t);
        });
        return map;
    }, [allTasks]);

    const categories = useMemo(() => {
        const cats = new Set(allTasks.map(t => t.category).filter(Boolean));
        return ['All', ...Array.from(cats).sort()];
    }, [allTasks]);

    // Current week tasks
    const currentWeekTasks = selectedWeek ? (tasksByWeek[selectedWeek.id] || []) : [];
    
    // Filtered tasks for selected week
    const filteredTasks = useMemo(() => {
        return currentWeekTasks.filter(task => {
            if (statusFilter === 'Pending' && task.completed) return false;
            if (statusFilter === 'Completed' && !task.completed) return false;
            
            if (categoryFilter !== 'All' && task.category !== categoryFilter) return false;
            
            if (searchQuery) {
                const q = searchQuery.toLowerCase();
                const matchesTitle = task.title.toLowerCase().includes(q);
                const matchesDesc = (task.description || '').toLowerCase().includes(q);
                const matchesCat = (task.category || '').toLowerCase().includes(q);
                if (!matchesTitle && !matchesDesc && !matchesCat) return false;
            }
            return true;
        });
    }, [currentWeekTasks, statusFilter, categoryFilter, searchQuery]);

    const currentWeekProgress = useMemo(() => {
        if (!selectedWeek) return { total: 0, completed: 0, pct: 0 };
        const total = currentWeekTasks.length;
        const completed = currentWeekTasks.filter(t => t.completed).length;
        const pct = total === 0 ? 0 : Math.round((completed / total) * 100);
        return { total, completed, pct };
    }, [currentWeekTasks, selectedWeek]);


    if (loadingData) {
        return <div style={{ padding: '20px', textAlign: 'center' }}>Loading roadmap and tasks...</div>;
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
            
            <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', alignItems: 'flex-start' }}>
                {/* Sidebar: Weeks List */}
                <div style={{ flex: '1 1 300px', minWidth: '250px' }}>
                    <h3 style={{ marginTop: 0 }}>Weeks</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        {weeks.map(week => {
                            const wTasks = tasksByWeek[week.id] || [];
                            const wTotal = wTasks.length;
                            const wCompleted = wTasks.filter(t => t.completed).length;
                            const wPct = wTotal === 0 ? 0 : Math.round((wCompleted / wTotal) * 100);

                            return (
                                <div 
                                    key={week.id} 
                                    onClick={() => {
                                        setSelectedWeek(week);
                                        setSearchQuery('');
                                        setStatusFilter('All');
                                        setCategoryFilter('All');
                                    }}
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
                                    <div style={{ fontSize: '14px', color: '#555', marginBottom: '8px' }}>{week.title}</div>
                                    
                                    <div style={{ fontSize: '12px', color: '#666', display: 'flex', justifyContent: 'space-between' }}>
                                        <span>{wCompleted} / {wTotal} tasks completed</span>
                                        <span style={{ fontWeight: 'bold' }}>{wPct}%</span>
                                    </div>
                                    <div style={{ marginTop: '5px', width: '100%', backgroundColor: '#e9ecef', borderRadius: '2px', height: '6px', overflow: 'hidden' }}>
                                        <div style={{ width: `${wPct}%`, backgroundColor: wPct === 100 ? '#28a745' : '#0066cc', height: '100%', transition: 'width 0.3s ease' }}></div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* Main Panel: Task List */}
                <div style={{ flex: '2 1 500px', backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '4px', border: '1px solid #dee2e6', minHeight: '400px' }}>
                    {!selectedWeek ? (
                        <div style={{ textAlign: 'center', color: '#777', marginTop: '50px' }}>
                            Select a week to view its tasks.
                        </div>
                    ) : (
                        <div>
                            <h3 style={{ marginTop: 0 }}>Week {selectedWeek.week_number}: {selectedWeek.title}</h3>
                            <p style={{ color: '#555', marginBottom: '15px' }}>{selectedWeek.description}</p>
                            
                            {/* Week Progress Bar */}
                            <div style={{ marginBottom: '25px', padding: '15px', backgroundColor: 'white', border: '1px solid #ddd', borderRadius: '4px' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px', fontSize: '14px' }}>
                                    <strong>Week Progress: {currentWeekProgress.completed} / {currentWeekProgress.total}</strong>
                                    <strong>{currentWeekProgress.pct}%</strong>
                                </div>
                                <div style={{ width: '100%', backgroundColor: '#e9ecef', borderRadius: '4px', height: '10px', overflow: 'hidden' }}>
                                    <div style={{ width: `${currentWeekProgress.pct}%`, backgroundColor: currentWeekProgress.pct === 100 ? '#28a745' : '#0066cc', height: '100%', transition: 'width 0.3s ease' }}></div>
                                </div>
                            </div>

                            {/* Filters & Search */}
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '20px' }}>
                                <input 
                                    type="text"
                                    placeholder="Search tasks..."
                                    value={searchQuery}
                                    onChange={e => setSearchQuery(e.target.value)}
                                    aria-label="Search tasks"
                                    style={{ flex: '1 1 200px', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                                />
                                <select 
                                    value={statusFilter} 
                                    onChange={e => setStatusFilter(e.target.value)}
                                    aria-label="Filter by status"
                                    style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                                >
                                    <option value="All">All Statuses</option>
                                    <option value="Pending">Pending</option>
                                    <option value="Completed">Completed</option>
                                </select>
                                <select 
                                    value={categoryFilter} 
                                    onChange={e => setCategoryFilter(e.target.value)}
                                    aria-label="Filter by category"
                                    style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
                                >
                                    {categories.map(cat => (
                                        <option key={cat} value={cat}>{cat === 'All' ? 'All Categories' : cat}</option>
                                    ))}
                                </select>
                            </div>
                            
                            {/* Task List */}
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                                {filteredTasks.length === 0 ? (
                                    <div style={{ padding: '20px', textAlign: 'center', backgroundColor: 'white', border: '1px dashed #ccc', color: '#777', borderRadius: '4px' }}>
                                        No tasks match the current filters.
                                    </div>
                                ) : (
                                    filteredTasks.map(task => (
                                        <label 
                                            key={task.id} 
                                            style={{ display: 'flex', alignItems: 'flex-start', gap: '15px', padding: '15px', backgroundColor: task.completed ? '#f0fdf4' : 'white', border: '1px solid', borderColor: task.completed ? '#c6f6d5' : '#ddd', borderRadius: '4px', cursor: updatingTask === task.id ? 'wait' : 'pointer', transition: 'background-color 0.2s' }}
                                        >
                                            <input 
                                                type="checkbox" 
                                                checked={task.completed}
                                                onChange={() => handleToggleTask(task)}
                                                disabled={updatingTask === task.id}
                                                aria-label={`Mark task ${task.title} as ${task.completed ? 'incomplete' : 'complete'}`}
                                                style={{ marginTop: '5px', width: '18px', height: '18px', cursor: updatingTask === task.id ? 'wait' : 'pointer' }}
                                            />
                                            <div style={{ flex: 1 }}>
                                                <div style={{ fontWeight: 'bold', textDecoration: task.completed ? 'line-through' : 'none', color: task.completed ? '#666' : '#000' }}>
                                                    {task.title}
                                                </div>
                                                {task.description && <div style={{ fontSize: '14px', color: '#555', marginTop: '5px' }}>{task.description}</div>}
                                                <div style={{ fontSize: '12px', color: '#888', marginTop: '8px', display: 'flex', flexWrap: 'wrap', gap: '15px' }}>
                                                    {task.category && <span style={{ backgroundColor: '#e2e8f0', padding: '2px 6px', borderRadius: '4px', color: '#4a5568' }}>{task.category}</span>}
                                                    {task.estimated_minutes && <span>⏱️ {task.estimated_minutes} min</span>}
                                                    {task.completed_at && <span style={{ color: '#28a745' }}>Completed</span>}
                                                </div>
                                            </div>
                                        </label>
                                    ))
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Roadmap;
