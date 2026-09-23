import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getDashboard } from '../services/api';
import { Link, useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchDashboard = async () => {
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const data = await getDashboard(token);
            setDashboardData(data);
        } catch (err) {
            setError(err.message || 'Failed to load dashboard data');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDashboard();
    }, []);

    if (loading) {
        return (
            <div style={{ padding: '30px', textAlign: 'center', color: '#666' }}>
                <p>Loading your preparation dashboard...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ padding: '20px', backgroundColor: '#fff5f5', border: '1px solid #fed7d7', borderRadius: '8px', color: '#c53030' }}>
                <h3 style={{ marginTop: 0 }}>Unable to load dashboard</h3>
                <p>{error}</p>
                <button 
                    onClick={fetchDashboard}
                    style={{ padding: '8px 16px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                >
                    Retry
                </button>
            </div>
        );
    }

    if (!dashboardData) {
        return null;
    }

    const { overall, current_week, today, categories, latest_assessment } = dashboardData;

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
            {/* Header / Welcome */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #eaeaea', paddingBottom: '15px', flexWrap: 'wrap', gap: '10px' }}>
                <div>
                    <h2 style={{ margin: 0, color: '#1e293b' }}>Preparation Dashboard</h2>
                    <p style={{ margin: '5px 0 0 0', color: '#64748b', fontSize: '14px' }}>
                        Welcome back, <strong>{user?.name || 'Candidate'}</strong>. Track your 12-week internship preparation progress.
                    </p>
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                        onClick={() => navigate('/app/roadmap', { state: { weekNumber: current_week.week_number } })}
                        style={{ padding: '10px 18px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', fontSize: '14px' }}
                    >
                        Continue Roadmap →
                    </button>
                </div>
            </div>

            {/* Top Cards Grid: Overall, Current Week, Today */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px' }}>
                
                {/* 1. Overall Progress */}
                <div style={{ padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                    <div>
                        <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                            Overall Progress
                        </div>
                        <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', marginTop: '10px' }}>
                            <span style={{ fontSize: '32px', fontWeight: 'bold', color: '#0f172a' }}>
                                {overall.completion_percentage}%
                            </span>
                            <span style={{ fontSize: '14px', color: '#64748b' }}>
                                ({overall.completed_tasks} / {overall.total_tasks} tasks)
                            </span>
                        </div>
                    </div>
                    <div style={{ marginTop: '15px' }}>
                        <div style={{ width: '100%', backgroundColor: '#e2e8f0', borderRadius: '4px', height: '8px', overflow: 'hidden' }}>
                            <div style={{ width: `${overall.completion_percentage}%`, backgroundColor: overall.completion_percentage === 100 ? '#28a745' : '#0066cc', height: '100%', transition: 'width 0.4s ease' }}></div>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#64748b', marginTop: '6px' }}>
                            <span>{overall.remaining_tasks} tasks remaining</span>
                            <span>Target: 204 tasks</span>
                        </div>
                    </div>
                </div>

                {/* 2. Current Week */}
                <div style={{ padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                    <div>
                        <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#0066cc', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                            Current Focus — Week {current_week.week_number}
                        </div>
                        <div style={{ fontWeight: '600', color: '#1e293b', fontSize: '16px', marginTop: '8px', minHeight: '40px' }}>
                            {current_week.title}
                        </div>
                    </div>
                    <div style={{ marginTop: '15px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '6px', color: '#475569' }}>
                            <span>Progress</span>
                            <strong>{current_week.completed_tasks} / {current_week.total_tasks} ({current_week.completion_percentage}%)</strong>
                        </div>
                        <div style={{ width: '100%', backgroundColor: '#e2e8f0', borderRadius: '4px', height: '8px', overflow: 'hidden' }}>
                            <div style={{ width: `${current_week.completion_percentage}%`, backgroundColor: current_week.completion_percentage === 100 ? '#28a745' : '#0284c7', height: '100%', transition: 'width 0.4s ease' }}></div>
                        </div>
                    </div>
                </div>

                {/* 3. Today's Preparation */}
                <div style={{ padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                    <div>
                        <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#059669', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                            Today's Schedule
                        </div>
                        <div style={{ fontWeight: '600', color: '#1e293b', fontSize: '16px', marginTop: '8px' }}>
                            Day {today.day_number} — {today.day_name}
                        </div>
                        <div style={{ fontSize: '14px', color: '#64748b', marginTop: '4px' }}>
                            {today.completed_tasks} of {today.task_count} tasks completed
                        </div>
                    </div>
                    <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
                        <button
                            onClick={() => navigate('/app/roadmap', { state: { weekNumber: current_week.week_number } })}
                            style={{ width: '100%', padding: '8px', backgroundColor: '#ffffff', color: '#0066cc', border: '1px solid #0066cc', borderRadius: '4px', cursor: 'pointer', fontSize: '13px', fontWeight: 'bold' }}
                        >
                            View Today's Tasks
                        </button>
                    </div>
                </div>

            </div>

            {/* Recent Assessment Summary Card */}
            {latest_assessment && (
                <div style={{ padding: '20px', backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '15px' }}>
                    <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px' }}>
                            <span style={{ fontSize: '12px', fontWeight: 'bold', color: '#0066cc', textTransform: 'uppercase' }}>
                                Recent Assessment Performance
                            </span>
                            <span style={{
                                fontSize: '11px',
                                fontWeight: 'bold',
                                padding: '2px 8px',
                                borderRadius: '4px',
                                backgroundColor: latest_assessment.passed ? '#dcfce7' : '#fee2e2',
                                color: latest_assessment.passed ? '#15803d' : '#991b1b'
                            }}>
                                {latest_assessment.passed ? '✓ PASSED' : '✕ NEEDS IMPROVEMENT'}
                            </span>
                        </div>
                        <h4 style={{ margin: '4px 0 0 0', color: '#0f172a', fontSize: '16px' }}>
                            {latest_assessment.assessment_title}
                        </h4>
                        <p style={{ margin: '4px 0 0 0', color: '#64748b', fontSize: '13px' }}>
                            Score: <strong>{latest_assessment.score} / {latest_assessment.total_marks}</strong> ({latest_assessment.percentage}%) • Completed on {new Date(latest_assessment.submitted_at).toLocaleDateString()}
                        </p>
                    </div>
                    <button
                        onClick={() => navigate('/app/assessments')}
                        style={{ padding: '8px 16px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '13px', fontWeight: 'bold' }}
                    >
                        Review Assessment & Mistakes →
                    </button>
                </div>
            )}

            {/* Category Progress Section */}
            <div style={{ padding: '25px', backgroundColor: 'white', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                <h3 style={{ margin: '0 0 15px 0', fontSize: '18px', color: '#1e293b' }}>
                    Curriculum Category Progress
                </h3>
                <p style={{ margin: '0 0 20px 0', color: '#64748b', fontSize: '14px' }}>
                    Breakdown of preparation completion across core interview domains.
                </p>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '15px' }}>
                    {categories.map(cat => (
                        <div key={cat.category} style={{ padding: '12px 15px', backgroundColor: '#f8fafc', borderRadius: '6px', border: '1px solid #f1f5f9' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                                <strong style={{ fontSize: '14px', color: '#334155' }}>{cat.category}</strong>
                                <span style={{ fontSize: '12px', fontWeight: 'bold', color: cat.completion_percentage === 100 ? '#28a745' : '#475569' }}>
                                    {cat.completion_percentage}%
                                </span>
                            </div>
                            <div style={{ width: '100%', backgroundColor: '#e2e8f0', borderRadius: '3px', height: '6px', overflow: 'hidden' }}>
                                <div style={{ width: `${cat.completion_percentage}%`, backgroundColor: cat.completion_percentage === 100 ? '#28a745' : '#0066cc', height: '100%', transition: 'width 0.3s ease' }}></div>
                            </div>
                            <div style={{ fontSize: '11px', color: '#94a3b8', marginTop: '5px', textAlign: 'right' }}>
                                {cat.completed_tasks} / {cat.total_tasks} tasks
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Quick Actions & Highlights */}
            <div style={{ padding: '20px', backgroundColor: '#f1f5f9', borderRadius: '8px', border: '1px solid #cbd5e1', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '15px' }}>
                <div>
                    <strong style={{ fontSize: '15px', color: '#1e293b', display: 'block' }}>Ready for your next study block?</strong>
                    <span style={{ fontSize: '13px', color: '#64748b' }}>Navigate to your structured roadmap to mark completed practice and theory items.</span>
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                        onClick={() => navigate('/app/roadmap')}
                        style={{ padding: '8px 16px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '14px', fontWeight: '500' }}
                    >
                        Open Full Roadmap
                    </button>
                    <button
                        onClick={() => navigate('/app/weaknesses')}
                        style={{ padding: '8px 16px', backgroundColor: '#ffffff', color: '#0066cc', border: '1px solid #0066cc', borderRadius: '4px', cursor: 'pointer', fontSize: '14px', fontWeight: '500' }}
                    >
                        Review Weak Areas
                    </button>
                    <button
                        onClick={() => navigate('/app/weekly-review', { state: { weekNumber: current_week.week_number } })}
                        style={{ padding: '8px 16px', backgroundColor: '#ffffff', color: '#0066cc', border: '1px solid #0066cc', borderRadius: '4px', cursor: 'pointer', fontSize: '14px', fontWeight: '500' }}
                    >
                        Weekly Review
                    </button>
                </div>

            </div>
        </div>
    );
};

export default Dashboard;
