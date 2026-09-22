import React, { useState, useEffect } from 'react';
import { getAssessments, getAssessmentAttempts, startAssessmentAttempt, submitAssessmentAnswer, submitAssessmentAttempt } from '../services/api';

const TYPE_COLORS = {
    BASELINE: { bg: '#e0e7ff', text: '#3730a3', border: '#c7d2fe' },
    QUIZ: { bg: '#e0f2fe', text: '#0369a1', border: '#bae6fd' },
    TIMED_CODING: { bg: '#fef3c7', text: '#92400e', border: '#fde68a' },
    MOCK: { bg: '#f3e8ff', text: '#6b21a8', border: '#e9d5ff' }
};

const DIFFICULTY_COLORS = {
    EASY: { bg: '#dcfce7', text: '#15803d' },
    MEDIUM: { bg: '#fef3c7', text: '#b45309' },
    HARD: { bg: '#fee2e2', text: '#b91c1c' }
};

const Assessments = () => {
    const [assessments, setAssessments] = useState([]);
    const [attempts, setAttempts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Active Attempt State
    const [activeAttempt, setActiveAttempt] = useState(null);
    const [activeQuestions, setActiveQuestions] = useState([]);
    const [currentQIndex, setCurrentQIndex] = useState(0);
    const [userAnswers, setUserAnswers] = useState({}); // { [qId]: selectedOption }
    const [savingAnswer, setSavingAnswer] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [attemptResult, setAttemptResult] = useState(null);

    const fetchData = async () => {
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const [assList, attList] = await Promise.all([
                getAssessments(token),
                getAssessmentAttempts(token)
            ]);
            setAssessments(assList);
            setAttempts(attList);
        } catch (err) {
            setError(err.message || 'Failed to load assessments data');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleStartAssessment = async (assessmentId) => {
        setError('');
        setLoading(true);
        try {
            const token = localStorage.getItem('token');
            const startData = await startAssessmentAttempt(token, assessmentId);
            setActiveAttempt(startData);
            setActiveQuestions(startData.questions || []);
            setCurrentQIndex(0);
            setUserAnswers({});
            setAttemptResult(null);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (err) {
            setError(err.message || 'Failed to start assessment');
        } finally {
            setLoading(false);
        }
    };

    const handleSelectOption = async (questionId, option) => {
        setUserAnswers(prev => ({ ...prev, [questionId]: option }));
        if (!activeAttempt) return;

        setSavingAnswer(true);
        try {
            const token = localStorage.getItem('token');
            await submitAssessmentAnswer(token, activeAttempt.attempt_id, questionId, option);
        } catch (err) {
            console.error('Failed to auto-save answer:', err);
        } finally {
            setSavingAnswer(false);
        }
    };

    const handleSubmitAssessment = async () => {
        const answeredCount = Object.keys(userAnswers).length;
        const totalCount = activeQuestions.length;
        if (answeredCount < totalCount) {
            const confirmSubmit = window.confirm(
                `You have answered ${answeredCount} of ${totalCount} questions. Unanswered questions will receive 0 marks. Submit anyway?`
            );
            if (!confirmSubmit) return;
        }

        setSubmitting(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const result = await submitAssessmentAttempt(token, activeAttempt.attempt_id);
            setAttemptResult(result);
            // Refresh past attempts list in background
            const updatedAttempts = await getAssessmentAttempts(token);
            setAttempts(updatedAttempts);
        } catch (err) {
            setError(err.message || 'Failed to submit assessment');
        } finally {
            setSubmitting(false);
        }
    };

    const handleExitAttempt = () => {
        setActiveAttempt(null);
        setActiveQuestions([]);
        setUserAnswers({});
        setAttemptResult(null);
        setCurrentQIndex(0);
        fetchData();
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #eaeaea', paddingBottom: '15px', flexWrap: 'wrap', gap: '15px' }}>
                <div>
                    <h2 style={{ margin: 0, color: '#1e293b' }}>Assessment Engine</h2>
                    <p style={{ margin: '5px 0 0 0', color: '#64748b', fontSize: '14px' }}>
                        Curriculum-aligned milestone quizzes, baseline diagnostics, and scoring history.
                    </p>
                </div>
            </div>

            {error && (
                <div style={{ padding: '12px 16px', backgroundColor: '#fff5f5', border: '1px solid #fed7d7', borderRadius: '6px', color: '#c53030', fontSize: '14px' }}>
                    {error}
                </div>
            )}

            {/* ACTIVE ATTEMPT RUNNER / MODAL */}
            {activeAttempt && !attemptResult && (
                <div style={{ padding: '25px', backgroundColor: '#ffffff', borderRadius: '8px', border: '2px solid #0066cc', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}>
                    {/* Active Header */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #e2e8f0', paddingBottom: '15px', marginBottom: '20px', flexWrap: 'wrap', gap: '10px' }}>
                        <div>
                            <span style={{ fontSize: '12px', fontWeight: 'bold', color: '#0066cc', textTransform: 'uppercase' }}>
                                Active Assessment — {activeAttempt.assessment_id}
                            </span>
                            <h3 style={{ margin: '4px 0 0 0', color: '#0f172a' }}>
                                Question {currentQIndex + 1} of {activeQuestions.length}
                            </h3>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            {savingAnswer && (
                                <span style={{ fontSize: '12px', color: '#64748b' }}>Saving answer...</span>
                            )}
                            <button
                                onClick={handleExitAttempt}
                                style={{ padding: '6px 12px', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '4px', cursor: 'pointer', fontSize: '13px' }}
                            >
                                Exit
                            </button>
                        </div>
                    </div>

                    {/* Question Nav Pills */}
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '20px' }}>
                        {activeQuestions.map((q, idx) => {
                            const isAnswered = Boolean(userAnswers[q.id]);
                            const isCurrent = idx === currentQIndex;
                            return (
                                <button
                                    key={q.id}
                                    onClick={() => setCurrentQIndex(idx)}
                                    style={{
                                        width: '32px',
                                        height: '32px',
                                        borderRadius: '4px',
                                        border: isCurrent ? '2px solid #0066cc' : '1px solid #cbd5e1',
                                        backgroundColor: isCurrent ? '#0066cc' : (isAnswered ? '#dcfce7' : '#ffffff'),
                                        color: isCurrent ? '#ffffff' : (isAnswered ? '#166534' : '#334155'),
                                        fontWeight: 'bold',
                                        fontSize: '12px',
                                        cursor: 'pointer'
                                    }}
                                >
                                    {idx + 1}
                                </button>
                            );
                        })}
                    </div>

                    {/* Current Question Body */}
                    {activeQuestions[currentQIndex] && (() => {
                        const q = activeQuestions[currentQIndex];
                        const diff = DIFFICULTY_COLORS[q.difficulty] || DIFFICULTY_COLORS.MEDIUM;
                        return (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                                <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
                                    <span style={{ fontSize: '12px', fontWeight: 'bold', padding: '2px 8px', borderRadius: '4px', backgroundColor: '#f1f5f9', color: '#334155' }}>
                                        {q.category} — {q.topic}
                                    </span>
                                    <span style={{ fontSize: '11px', fontWeight: 'bold', padding: '2px 6px', borderRadius: '4px', backgroundColor: diff.bg, color: diff.text }}>
                                        {q.difficulty}
                                    </span>
                                    <span style={{ fontSize: '12px', color: '#64748b' }}>
                                        {q.marks} Mark{q.marks > 1 ? 's' : ''}
                                    </span>
                                </div>

                                <div style={{ fontSize: '16px', fontWeight: '600', color: '#0f172a', lineHeight: '1.5' }}>
                                    {q.question}
                                </div>

                                {/* Options */}
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '10px' }}>
                                    {q.options.map((opt, optIdx) => {
                                        const isSelected = userAnswers[q.id] === opt;
                                        return (
                                            <label
                                                key={optIdx}
                                                onClick={() => handleSelectOption(q.id, opt)}
                                                style={{
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '12px',
                                                    padding: '12px 16px',
                                                    borderRadius: '6px',
                                                    border: isSelected ? '2px solid #0066cc' : '1px solid #e2e8f0',
                                                    backgroundColor: isSelected ? '#eff6ff' : '#f8fafc',
                                                    cursor: 'pointer',
                                                    transition: 'all 0.15s ease'
                                                }}
                                            >
                                                <input
                                                    type="radio"
                                                    name={`q_${q.id}`}
                                                    checked={isSelected}
                                                    onChange={() => handleSelectOption(q.id, opt)}
                                                    style={{ cursor: 'pointer' }}
                                                />
                                                <span style={{ fontSize: '14px', color: '#1e293b', fontWeight: isSelected ? '600' : 'normal' }}>
                                                    {opt}
                                                </span>
                                            </label>
                                        );
                                    })}
                                </div>

                                {/* Question Footer Controls */}
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '20px', paddingTop: '15px', borderTop: '1px solid #e2e8f0' }}>
                                    <button
                                        type="button"
                                        disabled={currentQIndex === 0}
                                        onClick={() => setCurrentQIndex(prev => Math.max(0, prev - 1))}
                                        style={{
                                            padding: '8px 16px',
                                            backgroundColor: '#f1f5f9',
                                            border: '1px solid #cbd5e1',
                                            borderRadius: '4px',
                                            cursor: currentQIndex === 0 ? 'not-allowed' : 'pointer',
                                            opacity: currentQIndex === 0 ? 0.5 : 1
                                        }}
                                    >
                                        ← Previous
                                    </button>

                                    <div style={{ display: 'flex', gap: '10px' }}>
                                        {currentQIndex < activeQuestions.length - 1 ? (
                                            <button
                                                type="button"
                                                onClick={() => setCurrentQIndex(prev => Math.min(activeQuestions.length - 1, prev + 1))}
                                                style={{ padding: '8px 18px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}
                                            >
                                                Next →
                                            </button>
                                        ) : (
                                            <button
                                                type="button"
                                                disabled={submitting}
                                                onClick={handleSubmitAssessment}
                                                style={{ padding: '8px 20px', backgroundColor: '#16a34a', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}
                                            >
                                                {submitting ? 'Submitting...' : 'Submit Assessment ✓'}
                                            </button>
                                        )}
                                    </div>
                                </div>
                            </div>
                        );
                    })()}
                </div>
            )}

            {/* ATTEMPT RESULT BANNER */}
            {attemptResult && (
                <div style={{
                    padding: '25px',
                    borderRadius: '8px',
                    backgroundColor: attemptResult.passed ? '#f0fdf4' : '#fff5f5',
                    border: `2px solid ${attemptResult.passed ? '#22c55e' : '#ef4444'}`,
                    boxShadow: '0 4px 6px rgba(0,0,0,0.05)'
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '15px' }}>
                        <div>
                            <span style={{
                                display: 'inline-block',
                                padding: '4px 10px',
                                borderRadius: '12px',
                                fontSize: '13px',
                                fontWeight: 'bold',
                                backgroundColor: attemptResult.passed ? '#dcfce7' : '#fee2e2',
                                color: attemptResult.passed ? '#15803d' : '#991b1b',
                                marginBottom: '8px'
                            }}>
                                {attemptResult.passed ? '✓ PASSED' : '✕ NEEDS IMPROVEMENT'}
                            </span>
                            <h3 style={{ margin: 0, color: '#0f172a' }}>Assessment Completed</h3>
                            <p style={{ margin: '6px 0 0 0', color: '#475569', fontSize: '14px' }}>
                                Score: <strong>{attemptResult.score} / {attemptResult.total_marks}</strong> ({attemptResult.percentage}%)
                            </p>
                        </div>
                        <button
                            onClick={handleExitAttempt}
                            style={{ padding: '10px 20px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer' }}
                        >
                            Return to Assessments
                        </button>
                    </div>
                </div>
            )}

            {/* AVAILABLE ASSESSMENTS SECTION */}
            {!activeAttempt && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                    <h3 style={{ margin: '0 0 5px 0', color: '#1e293b' }}>Available Assessments</h3>
                    {loading ? (
                        <div style={{ padding: '30px', textAlign: 'center', color: '#64748b' }}>
                            Loading assessments...
                        </div>
                    ) : assessments.length === 0 ? (
                        <div style={{ padding: '30px', textAlign: 'center', backgroundColor: '#f8fafc', borderRadius: '8px', color: '#64748b' }}>
                            No published assessments available.
                        </div>
                    ) : (
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '18px' }}>
                            {assessments.map(ass => {
                                const typeStyle = TYPE_COLORS[ass.assessment_type] || TYPE_COLORS.QUIZ;
                                return (
                                    <div
                                        key={ass.id}
                                        style={{
                                            padding: '20px',
                                            backgroundColor: '#ffffff',
                                            borderRadius: '8px',
                                            border: '1px solid #e2e8f0',
                                            display: 'flex',
                                            flexDirection: 'column',
                                            justifyContent: 'space-between',
                                            boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
                                        }}
                                    >
                                        <div>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                                                <span style={{ fontSize: '11px', fontWeight: 'bold', padding: '2px 8px', borderRadius: '4px', backgroundColor: typeStyle.bg, color: typeStyle.text, border: `1px solid ${typeStyle.border}` }}>
                                                    {ass.assessment_type}
                                                </span>
                                                {ass.week_number && (
                                                    <span style={{ fontSize: '12px', fontWeight: 'bold', color: '#64748b' }}>
                                                        Week {ass.week_number}
                                                    </span>
                                                )}
                                            </div>
                                            <h4 style={{ margin: '0 0 8px 0', color: '#0f172a', fontSize: '16px' }}>
                                                {ass.title}
                                            </h4>
                                            <p style={{ margin: '0 0 15px 0', fontSize: '13px', color: '#64748b', lineHeight: '1.4' }}>
                                                {ass.description}
                                            </p>
                                        </div>

                                        <div>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#64748b', marginBottom: '12px', borderTop: '1px solid #f1f5f9', paddingTop: '10px' }}>
                                                <span>⏱️ {ass.duration_minutes} mins</span>
                                                <span>📝 {ass.question_count} Questions</span>
                                                <span>🎯 Pass: {ass.passing_score}%</span>
                                            </div>
                                            <button
                                                onClick={() => handleStartAssessment(ass.id)}
                                                style={{ width: '100%', padding: '9px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', fontSize: '13px' }}
                                            >
                                                Start Assessment →
                                            </button>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>
            )}

            {/* PREVIOUS ATTEMPTS SECTION */}
            {!activeAttempt && (
                <div style={{ padding: '25px', backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                    <h3 style={{ margin: '0 0 15px 0', color: '#1e293b' }}>Previous Attempts</h3>
                    {attempts.length === 0 ? (
                        <div style={{ padding: '30px', textAlign: 'center', backgroundColor: '#f8fafc', borderRadius: '6px', color: '#64748b', fontSize: '13px' }}>
                            No attempts recorded yet. Select an assessment above to begin!
                        </div>
                    ) : (
                        <div style={{ overflowX: 'auto' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
                                <thead>
                                    <tr style={{ borderBottom: '2px solid #e2e8f0', color: '#475569' }}>
                                        <th style={{ padding: '10px' }}>Assessment</th>
                                        <th style={{ padding: '10px' }}>Date</th>
                                        <th style={{ padding: '10px' }}>Score</th>
                                        <th style={{ padding: '10px' }}>Percentage</th>
                                        <th style={{ padding: '10px' }}>Status</th>
                                        <th style={{ padding: '10px' }}>Result</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {attempts.map(att => (
                                        <tr key={att.attempt_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                                            <td style={{ padding: '12px 10px', fontWeight: '600', color: '#0f172a' }}>
                                                {att.assessment_title}
                                            </td>
                                            <td style={{ padding: '12px 10px', color: '#64748b' }}>
                                                {new Date(att.started_at).toLocaleDateString()} {new Date(att.started_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                            </td>
                                            <td style={{ padding: '12px 10px' }}>
                                                {att.score !== null && att.score !== undefined ? `${att.score} / ${att.total_marks}` : '—'}
                                            </td>
                                            <td style={{ padding: '12px 10px', fontWeight: 'bold' }}>
                                                {att.percentage !== null && att.percentage !== undefined ? `${att.percentage}%` : '—'}
                                            </td>
                                            <td style={{ padding: '12px 10px' }}>
                                                <span style={{
                                                    fontSize: '11px',
                                                    fontWeight: 'bold',
                                                    padding: '2px 6px',
                                                    borderRadius: '4px',
                                                    backgroundColor: att.status === 'SUBMITTED' ? '#dcfce7' : '#fef3c7',
                                                    color: att.status === 'SUBMITTED' ? '#15803d' : '#92400e'
                                                }}>
                                                    {att.status}
                                                </span>
                                            </td>
                                            <td style={{ padding: '12px 10px' }}>
                                                {att.status === 'SUBMITTED' ? (
                                                    <span style={{
                                                        fontSize: '11px',
                                                        fontWeight: 'bold',
                                                        padding: '2px 6px',
                                                        borderRadius: '4px',
                                                        backgroundColor: att.passed ? '#dcfce7' : '#fee2e2',
                                                        color: att.passed ? '#15803d' : '#991b1b'
                                                    }}>
                                                        {att.passed ? 'PASSED' : 'FAILED'}
                                                    </span>
                                                ) : (
                                                    <span style={{ color: '#94a3b8' }}>In Progress</span>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Assessments;
