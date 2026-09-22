import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { getWeaknesses, createWeakness, updateWeakness, deleteWeakness } from '../services/api';


const PRIORITY_COLORS = {
    CRITICAL: { bg: '#fee2e2', text: '#991b1b', border: '#f87171' },
    HIGH: { bg: '#ffedd5', text: '#9a3412', border: '#fb923c' },
    MEDIUM: { bg: '#e0f2fe', text: '#0369a1', border: '#38bdf8' },
    LOW: { bg: '#f1f5f9', text: '#475569', border: '#cbd5e1' }
};

const STATUS_COLORS = {
    OPEN: { bg: '#fef3c7', text: '#92400e', border: '#fcd34d' },
    REVIEWED: { bg: '#e0e7ff', text: '#3730a3', border: '#a5b4fc' },
    RESOLVED: { bg: '#dcfce7', text: '#166534', border: '#86efac' }
};

const Weaknesses = () => {
    const navigate = useNavigate();
    const [weaknesses, setWeaknesses] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [actionLoading, setActionLoading] = useState(false);

    // Filter states
    const [statusFilter, setStatusFilter] = useState('ALL');
    const [priorityFilter, setPriorityFilter] = useState('ALL');
    const [topicFilter, setTopicFilter] = useState('ALL');
    const [searchQuery, setSearchQuery] = useState('');

    // Form states
    const [showForm, setShowForm] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [formData, setFormData] = useState({
        topic: '',
        problem_concept: '',
        what_i_got_wrong: '',
        correct_concept: '',
        priority: 'MEDIUM',
        retry_date: ''
    });

    const fetchItems = async () => {
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const data = await getWeaknesses(token);
            setWeaknesses(data);
        } catch (err) {
            setError(err.message || 'Failed to load weaknesses');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchItems();
    }, []);

    // Summary calculation
    const summary = useMemo(() => {
        const today = new Date().toISOString().split('T')[0];
        let openCount = 0;
        let highPriorityCount = 0;
        let dueCount = 0;
        let resolvedCount = 0;

        weaknesses.forEach(w => {
            if (w.status === 'RESOLVED') {
                resolvedCount++;
            } else {
                openCount++;
                if (w.priority === 'HIGH' || w.priority === 'CRITICAL') {
                    highPriorityCount++;
                }
                if (w.retry_date) {
                    const rDate = w.retry_date.split('T')[0];
                    if (rDate <= today) {
                        dueCount++;
                    }
                }
            }
        });

        return { openCount, highPriorityCount, dueCount, resolvedCount };
    }, [weaknesses]);

    // Dynamic topics
    const uniqueTopics = useMemo(() => {
        const set = new Set(weaknesses.map(w => w.topic).filter(Boolean));
        return ['ALL', ...Array.from(set).sort()];
    }, [weaknesses]);

    // Filtered items
    const filteredWeaknesses = useMemo(() => {
        const q = searchQuery.toLowerCase().trim();
        return weaknesses.filter(w => {
            if (statusFilter !== 'ALL' && w.status !== statusFilter) return false;
            if (priorityFilter !== 'ALL' && w.priority !== priorityFilter) return false;
            if (topicFilter !== 'ALL' && w.topic !== topicFilter) return false;

            if (q) {
                const matchTopic = (w.topic || '').toLowerCase().includes(q);
                const matchProb = (w.problem_concept || '').toLowerCase().includes(q);
                const matchWrong = (w.what_i_got_wrong || '').toLowerCase().includes(q);
                const matchRight = (w.correct_concept || '').toLowerCase().includes(q);
                if (!matchTopic && !matchProb && !matchWrong && !matchRight) return false;
            }
            return true;
        });
    }, [weaknesses, statusFilter, priorityFilter, topicFilter, searchQuery]);

    const handleFormChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleStartAdd = () => {
        setEditingId(null);
        setFormData({
            topic: '',
            problem_concept: '',
            what_i_got_wrong: '',
            correct_concept: '',
            priority: 'MEDIUM',
            retry_date: ''
        });
        setShowForm(true);
    };

    const handleStartEdit = (w) => {
        setEditingId(w.id);
        setFormData({
            topic: w.topic,
            problem_concept: w.problem_concept,
            what_i_got_wrong: w.what_i_got_wrong,
            correct_concept: w.correct_concept,
            priority: w.priority,
            retry_date: w.retry_date ? w.retry_date.split('T')[0] : ''
        });
        setShowForm(true);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleSubmitForm = async (e) => {
        e.preventDefault();
        setError('');
        setActionLoading(true);
        try {
            const token = localStorage.getItem('token');
            const payload = {
                topic: formData.topic.trim(),
                problem_concept: formData.problem_concept.trim(),
                what_i_got_wrong: formData.what_i_got_wrong.trim(),
                correct_concept: formData.correct_concept.trim(),
                priority: formData.priority,
                retry_date: formData.retry_date ? new Date(formData.retry_date).toISOString() : null
            };

            if (editingId) {
                const updated = await updateWeakness(token, editingId, payload);
                setWeaknesses(prev => prev.map(w => w.id === editingId ? updated : w));
            } else {
                const created = await createWeakness(token, payload);
                setWeaknesses(prev => [created, ...prev]);
            }
            setShowForm(false);
            setEditingId(null);
        } catch (err) {
            setError(err.message || 'Failed to save weakness');
        } finally {
            setActionLoading(false);
        }
    };

    const handleUpdateStatus = async (id, newStatus) => {
        setActionLoading(true);
        try {
            const token = localStorage.getItem('token');
            const updated = await updateWeakness(token, id, { status: newStatus });
            setWeaknesses(prev => prev.map(w => w.id === id ? updated : w));
        } catch (err) {
            setError(err.message || `Failed to update status to ${newStatus}`);
        } finally {
            setActionLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this weakness record?')) return;
        setActionLoading(true);
        try {
            const token = localStorage.getItem('token');
            await deleteWeakness(token, id);
            setWeaknesses(prev => prev.filter(w => w.id !== id));
        } catch (err) {
            setError(err.message || 'Failed to delete weakness');
        } finally {
            setActionLoading(false);
        }
    };

    const isDue = (item) => {
        if (!item.retry_date || item.status === 'RESOLVED') return false;
        const today = new Date().toISOString().split('T')[0];
        return item.retry_date.split('T')[0] <= today;
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #eaeaea', paddingBottom: '15px', flexWrap: 'wrap', gap: '15px' }}>
                <div>
                    <h2 style={{ margin: 0, color: '#1e293b' }}>Weakness Manager & Mistake Log</h2>
                    <p style={{ margin: '5px 0 0 0', color: '#64748b', fontSize: '14px' }}>
                        Log conceptual errors, track recurring weaknesses, and schedule timely retries.
                    </p>
                </div>
                <div>
                    <button
                        onClick={() => {
                            if (showForm) {
                                setShowForm(false);
                                setEditingId(null);
                            } else {
                                handleStartAdd();
                            }
                        }}
                        style={{ padding: '10px 18px', backgroundColor: showForm ? '#64748b' : '#0066cc', color: 'white', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', fontSize: '14px' }}
                    >
                        {showForm ? 'Cancel' : '+ Log Weakness'}
                    </button>
                </div>
            </div>

            {error && (
                <div style={{ padding: '12px 16px', backgroundColor: '#fff5f5', border: '1px solid #fed7d7', borderRadius: '6px', color: '#c53030', fontSize: '14px' }}>
                    {error}
                </div>
            )}

            {/* KPI Summary Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '15px' }}>
                <div style={{ padding: '15px 20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                    <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#64748b', textTransform: 'uppercase' }}>Open Weaknesses</div>
                    <div style={{ fontSize: '26px', fontWeight: 'bold', color: '#0f172a', marginTop: '6px' }}>{summary.openCount}</div>
                </div>
                <div style={{ padding: '15px 20px', backgroundColor: '#fff7ed', borderRadius: '8px', border: '1px solid #fed7aa' }}>
                    <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#c2410c', textTransform: 'uppercase' }}>High / Critical</div>
                    <div style={{ fontSize: '26px', fontWeight: 'bold', color: '#9a3412', marginTop: '6px' }}>{summary.highPriorityCount}</div>
                </div>
                <div style={{ padding: '15px 20px', backgroundColor: '#fef2f2', borderRadius: '8px', border: '1px solid #fecaca' }}>
                    <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#b91c1c', textTransform: 'uppercase' }}>Due for Review</div>
                    <div style={{ fontSize: '26px', fontWeight: 'bold', color: '#991b1b', marginTop: '6px' }}>{summary.dueCount}</div>
                </div>
                <div style={{ padding: '15px 20px', backgroundColor: '#f0fdf4', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
                    <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#15803d', textTransform: 'uppercase' }}>Resolved</div>
                    <div style={{ fontSize: '26px', fontWeight: 'bold', color: '#166534', marginTop: '6px' }}>{summary.resolvedCount}</div>
                </div>
            </div>

            {/* Create / Edit Form Modal / Box */}
            {showForm && (
                <div style={{ padding: '25px', backgroundColor: '#ffffff', borderRadius: '8px', border: '2px solid #0066cc', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
                    <h3 style={{ margin: '0 0 15px 0', color: '#1e293b' }}>
                        {editingId ? 'Edit Weakness Record' : 'Log New Weakness / Mistake'}
                    </h3>
                    <form onSubmit={handleSubmitForm} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '15px' }}>
                            <div>
                                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', marginBottom: '5px', color: '#334155' }}>
                                    Topic *
                                </label>
                                <input
                                    type="text"
                                    name="topic"
                                    placeholder="e.g. Dynamic Programming, SQL Joins, Binary Search"
                                    value={formData.topic}
                                    onChange={handleFormChange}
                                    required
                                    style={{ width: '100%', padding: '9px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' }}
                                />
                            </div>

                            <div>
                                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', marginBottom: '5px', color: '#334155' }}>
                                    Problem / Concept *
                                </label>
                                <input
                                    type="text"
                                    name="problem_concept"
                                    placeholder="e.g. LC 300 Longest Increasing Subsequence / Left Join Nulls"
                                    value={formData.problem_concept}
                                    onChange={handleFormChange}
                                    required
                                    style={{ width: '100%', padding: '9px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' }}
                                />
                            </div>
                        </div>

                        <div>
                            <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', marginBottom: '5px', color: '#334155' }}>
                                What I Got Wrong *
                            </label>
                            <textarea
                                name="what_i_got_wrong"
                                rows="3"
                                placeholder="Explain the misconception or mistake made during problem solving..."
                                value={formData.what_i_got_wrong}
                                onChange={handleFormChange}
                                required
                                style={{ width: '100%', padding: '9px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' }}
                            />
                        </div>

                        <div>
                            <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', marginBottom: '5px', color: '#334155' }}>
                                Correct Concept / Key Takeaway *
                            </label>
                            <textarea
                                name="correct_concept"
                                rows="3"
                                placeholder="Write the correct mental model, formula, or optimization approach..."
                                value={formData.correct_concept}
                                onChange={handleFormChange}
                                required
                                style={{ width: '100%', padding: '9px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' }}
                            />
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
                            <div>
                                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', marginBottom: '5px', color: '#334155' }}>
                                    Priority *
                                </label>
                                <select
                                    name="priority"
                                    value={formData.priority}
                                    onChange={handleFormChange}
                                    style={{ width: '100%', padding: '9px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', backgroundColor: 'white' }}
                                >
                                    <option value="LOW">LOW</option>
                                    <option value="MEDIUM">MEDIUM</option>
                                    <option value="HIGH">HIGH</option>
                                    <option value="CRITICAL">CRITICAL</option>
                                </select>
                            </div>

                            <div>
                                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', marginBottom: '5px', color: '#334155' }}>
                                    Retry Date
                                </label>
                                <input
                                    type="date"
                                    name="retry_date"
                                    value={formData.retry_date}
                                    onChange={handleFormChange}
                                    style={{ width: '100%', padding: '8px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' }}
                                />
                            </div>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
                            <button
                                type="button"
                                onClick={() => { setShowForm(false); setEditingId(null); }}
                                style={{ padding: '9px 18px', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '4px', cursor: 'pointer', fontSize: '14px' }}
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={actionLoading}
                                style={{ padding: '9px 20px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer', fontSize: '14px' }}
                            >
                                {actionLoading ? 'Saving...' : (editingId ? 'Update Weakness' : 'Save Weakness')}
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {/* Filter Bar */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', padding: '15px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', alignItems: 'center' }}>
                <input
                    type="text"
                    placeholder="Search by topic, mistake, or concept..."
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    style={{ flex: '1 1 200px', padding: '8px 12px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px' }}
                />

                <select
                    value={statusFilter}
                    onChange={e => setStatusFilter(e.target.value)}
                    aria-label="Filter by status"
                    style={{ padding: '8px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', backgroundColor: 'white' }}
                >
                    <option value="ALL">All Statuses</option>
                    <option value="OPEN">Open</option>
                    <option value="REVIEWED">Reviewed</option>
                    <option value="RESOLVED">Resolved</option>
                </select>

                <select
                    value={priorityFilter}
                    onChange={e => setPriorityFilter(e.target.value)}
                    aria-label="Filter by priority"
                    style={{ padding: '8px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', backgroundColor: 'white' }}
                >
                    <option value="ALL">All Priorities</option>
                    <option value="CRITICAL">Critical</option>
                    <option value="HIGH">High</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="LOW">Low</option>
                </select>

                <select
                    value={topicFilter}
                    onChange={e => setTopicFilter(e.target.value)}
                    aria-label="Filter by topic"
                    style={{ padding: '8px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', backgroundColor: 'white' }}
                >
                    {uniqueTopics.map(t => (
                        <option key={t} value={t}>{t === 'ALL' ? 'All Topics' : t}</option>
                    ))}
                </select>
            </div>

            {/* Weaknesses List */}
            {loading ? (
                <div style={{ padding: '30px', textAlign: 'center', color: '#64748b' }}>
                    Loading weaknesses...
                </div>
            ) : filteredWeaknesses.length === 0 ? (
                <div style={{ padding: '40px 20px', textAlign: 'center', backgroundColor: '#f8fafc', border: '1px dashed #cbd5e1', borderRadius: '8px', color: '#64748b' }}>
                    <h4 style={{ margin: '0 0 8px 0', color: '#334155' }}>No weaknesses found</h4>
                    <p style={{ margin: 0, fontSize: '14px' }}>
                        {weaknesses.length === 0 
                            ? 'You have not logged any mistakes or weaknesses yet. Click "+ Log Weakness" to start tracking.'
                            : 'No items match your active search and filter criteria.'}
                    </p>
                </div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                    {filteredWeaknesses.map(item => {
                        const pri = PRIORITY_COLORS[item.priority] || PRIORITY_COLORS.MEDIUM;
                        const sta = STATUS_COLORS[item.status] || STATUS_COLORS.OPEN;
                        const due = isDue(item);

                        return (
                            <div 
                                key={item.id}
                                style={{ 
                                    backgroundColor: 'white', 
                                    border: due ? '2px solid #ef4444' : '1px solid #e2e8f0', 
                                    borderRadius: '8px', 
                                    padding: '18px 20px',
                                    boxShadow: '0 1px 3px rgba(0,0,0,0.05)' 
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '10px', marginBottom: '12px' }}>
                                    <div>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                                            <span style={{ fontSize: '16px', fontWeight: 'bold', color: '#0f172a' }}>
                                                {item.topic}
                                            </span>
                                            <span style={{ fontSize: '12px', fontWeight: 'bold', padding: '2px 8px', borderRadius: '4px', backgroundColor: pri.bg, color: pri.text, border: `1px solid ${pri.border}` }}>
                                                {item.priority}
                                            </span>
                                            <span style={{ fontSize: '12px', fontWeight: 'bold', padding: '2px 8px', borderRadius: '4px', backgroundColor: sta.bg, color: sta.text, border: `1px solid ${sta.border}` }}>
                                                {item.status}
                                            </span>
                                            {due && (
                                                <span style={{ fontSize: '11px', fontWeight: 'bold', padding: '2px 6px', borderRadius: '4px', backgroundColor: '#fee2e2', color: '#dc2626' }}>
                                                    ⚠️ Due for Review
                                                </span>
                                            )}
                                        </div>
                                        <div style={{ fontSize: '14px', color: '#475569', marginTop: '4px', fontWeight: '500' }}>
                                            {item.problem_concept}
                                        </div>
                                    </div>

                                    <div style={{ fontSize: '12px', color: '#64748b' }}>
                                        {item.retry_date && (
                                            <span style={{ marginRight: '15px' }}>
                                                🗓️ Retry: <strong>{item.retry_date.split('T')[0]}</strong>
                                            </span>
                                        )}
                                        <span>Logged: {item.date ? item.date.split('T')[0] : item.created_at.split('T')[0]}</span>
                                    </div>
                                </div>

                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '15px', marginTop: '10px', backgroundColor: '#f8fafc', padding: '12px 15px', borderRadius: '6px' }}>
                                    <div>
                                        <strong style={{ fontSize: '12px', color: '#dc2626', textTransform: 'uppercase', display: 'block', marginBottom: '4px' }}>
                                            ❌ What I Got Wrong
                                        </strong>
                                        <p style={{ margin: 0, fontSize: '13px', color: '#334155', whiteSpace: 'pre-wrap' }}>
                                            {item.what_i_got_wrong}
                                        </p>
                                    </div>
                                    <div>
                                        <strong style={{ fontSize: '12px', color: '#16a34a', textTransform: 'uppercase', display: 'block', marginBottom: '4px' }}>
                                            ✅ Correct Concept / Strategy
                                        </strong>
                                        <p style={{ margin: 0, fontSize: '13px', color: '#334155', whiteSpace: 'pre-wrap' }}>
                                            {item.correct_concept}
                                        </p>
                                    </div>
                                </div>

                                {/* Actions Bar */}
                                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '14px', paddingTop: '10px', borderTop: '1px solid #f1f5f9' }}>
                                    {item.status !== 'REVIEWED' && item.status !== 'RESOLVED' && (
                                        <button
                                            onClick={() => handleUpdateStatus(item.id, 'REVIEWED')}
                                            disabled={actionLoading}
                                            style={{ padding: '5px 12px', backgroundColor: '#e0e7ff', color: '#3730a3', border: '1px solid #c7d2fe', borderRadius: '4px', fontSize: '12px', fontWeight: '500', cursor: 'pointer' }}
                                        >
                                            Mark Reviewed
                                        </button>
                                    )}
                                    {item.status !== 'RESOLVED' && (
                                        <button
                                            onClick={() => handleUpdateStatus(item.id, 'RESOLVED')}
                                            disabled={actionLoading}
                                            style={{ padding: '5px 12px', backgroundColor: '#dcfce7', color: '#15803d', border: '1px solid #bbf7d0', borderRadius: '4px', fontSize: '12px', fontWeight: '500', cursor: 'pointer' }}
                                        >
                                            Mark Resolved
                                        </button>
                                    )}
                                    {item.status === 'RESOLVED' && (
                                        <button
                                            onClick={() => handleUpdateStatus(item.id, 'OPEN')}
                                            disabled={actionLoading}
                                            style={{ padding: '5px 12px', backgroundColor: '#fef3c7', color: '#92400e', border: '1px solid #fde68a', borderRadius: '4px', fontSize: '12px', fontWeight: '500', cursor: 'pointer' }}
                                        >
                                            Re-open
                                        </button>
                                    )}
                                    <button
                                        onClick={() => handleStartEdit(item)}
                                        disabled={actionLoading}
                                        style={{ padding: '5px 12px', backgroundColor: '#f1f5f9', color: '#334155', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '12px', fontWeight: '500', cursor: 'pointer' }}
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => handleDelete(item.id)}
                                        disabled={actionLoading}
                                        style={{ padding: '5px 12px', backgroundColor: '#fee2e2', color: '#991b1b', border: '1px solid #fecaca', borderRadius: '4px', fontSize: '12px', fontWeight: '500', cursor: 'pointer' }}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            {/* Weekly Review Section */}
            <div style={{ padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', marginTop: '10px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
                    <div>
                        <strong style={{ fontSize: '15px', color: '#1e293b' }}>Weekly Review & Retrospective</strong>
                        <p style={{ margin: '4px 0 0 0', fontSize: '13px', color: '#64748b' }}>
                            Synthesize weekly target completion, review top mistakes, and set your action plan.
                        </p>
                    </div>
                    <button
                        onClick={() => navigate('/app/weekly-review')}
                        style={{ padding: '8px 16px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '13px', fontWeight: 'bold' }}
                    >
                        Open Weekly Review →
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Weaknesses;

