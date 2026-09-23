import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    getAssessments,
    getAssessmentAttempts,
    startAssessmentAttempt,
    submitAssessmentAnswer,
    submitAssessmentAttempt,
    getAssessmentResult,
    createWeaknessFromAttempt
} from '../services/api';

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
    const navigate = useNavigate();
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

    // Detailed Result & Mistake Review State
    const [detailedResult, setDetailedResult] = useState(null);
    const [resultFilter, setResultFilter] = useState('ALL'); // 'ALL', 'MISTAKES', 'CORRECT'
    const [addingWeaknessId, setAddingWeaknessId] = useState(null);
    const [weaknessSuccessMsg, setWeaknessSuccessMsg] = useState('');

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
            setDetailedResult(null);
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
            await submitAssessmentAttempt(token, activeAttempt.attempt_id);
            // Fetch detailed result immediately after submission
            const fullResult = await getAssessmentResult(token, activeAttempt.attempt_id);
            setActiveAttempt(null);
            setDetailedResult(fullResult);
            // Refresh past attempts list in background
            const updatedAttempts = await getAssessmentAttempts(token);
            setAttempts(updatedAttempts);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (err) {
            setError(err.message || 'Failed to submit assessment');
        } finally {
            setSubmitting(false);
        }
    };

    const handleViewResult = async (attemptId) => {
        setError('');
        setLoading(true);
        try {
            const token = localStorage.getItem('token');
            const fullResult = await getAssessmentResult(token, attemptId);
            setDetailedResult(fullResult);
            setActiveAttempt(null);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (err) {
            setError(err.message || 'Failed to load assessment result');
        } finally {
            setLoading(false);
        }
    };

    const handleExitAttempt = () => {
        setActiveAttempt(null);
        setActiveQuestions([]);
        setUserAnswers({});
        setDetailedResult(null);
        setCurrentQIndex(0);
        fetchData();
    };

    const handleAddToWeaknesses = async (question) => {
        if (!detailedResult) return;
        setAddingWeaknessId(question.question_id);
        setError('');
        setWeaknessSuccessMsg('');
        try {
            const token = localStorage.getItem('token');
            await createWeaknessFromAttempt(token, detailedResult.attempt_id, {
                question_id: question.question_id,
                priority: 'HIGH'
            });

            // Update question in local state
            setDetailedResult(prev => {
                if (!prev) return prev;
                return {
                    ...prev,
                    questions: prev.questions.map(q =>
                        q.question_id === question.question_id
                            ? { ...q, is_in_weaknesses: true }
                            : q
                    )
                };
            });
            setWeaknessSuccessMsg(`Added mistake from "${question.topic}" to Weakness Manager.`);
            setTimeout(() => setWeaknessSuccessMsg(''), 4000);
        } catch (err) {
            setError(err.message || 'Failed to add weakness');
        } finally {
            setAddingWeaknessId(null);
        }
    };

    // Filter questions in detailed results
    const filteredQuestions = detailedResult ? detailedResult.questions.filter(q => {
        if (resultFilter === 'MISTAKES') return !q.is_correct;
        if (resultFilter === 'CORRECT') return q.is_correct;
        return true;
    }) : [];

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #eaeaea', paddingBottom: '15px', flexWrap: 'wrap', gap: '15px' }}>
                <div>
                    <h2 style={{ margin: 0, color: '#1e293b' }}>Assessment Engine</h2>
                    <p style={{ margin: '5px 0 0 0', color: '#64748b', fontSize: '14px' }}>
                        Curriculum-aligned milestone quizzes, baseline diagnostics, score breakdown, and mistake analysis.
                    </p>
                </div>
                {detailedResult && (
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <button
                            onClick={() => navigate('/app/weaknesses')}
                            style={{ padding: '8px 14px', backgroundColor: '#f1f5f9', color: '#0066cc', border: '1px solid #cbd5e1', borderRadius: '6px', fontSize: '13px', fontWeight: '500', cursor: 'pointer' }}
                        >
                            Open Weakness Manager →
                        </button>
                    </div>
                )}
            </div>

            {error && (
                <div style={{ padding: '12px 16px', backgroundColor: '#fff5f5', border: '1px solid #fed7d7', borderRadius: '6px', color: '#c53030', fontSize: '14px' }}>
                    {error}
                </div>
            )}

            {weaknessSuccessMsg && (
                <div style={{ padding: '12px 16px', backgroundColor: '#dcfce7', border: '1px solid #86efac', borderRadius: '6px', color: '#166534', fontSize: '14px' }}>
                    ✓ {weaknessSuccessMsg}
                </div>
            )}

            {/* ACTIVE ATTEMPT RUNNER / MODAL */}
            {activeAttempt && !detailedResult && (
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

            {/* DETAILED RESULTS & MISTAKE REVIEW SCREEN */}
            {detailedResult && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    {/* Results Overview Banner */}
                    <div style={{
                        padding: '25px',
                        borderRadius: '8px',
                        backgroundColor: detailedResult.passed ? '#f0fdf4' : '#fff5f5',
                        border: `2px solid ${detailedResult.passed ? '#22c55e' : '#ef4444'}`,
                        boxShadow: '0 4px 6px rgba(0,0,0,0.05)'
                    }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '15px' }}>
                            <div>
                                <span style={{
                                    display: 'inline-block',
                                    padding: '4px 10px',
                                    borderRadius: '12px',
                                    fontSize: '13px',
                                    fontWeight: 'bold',
                                    backgroundColor: detailedResult.passed ? '#dcfce7' : '#fee2e2',
                                    color: detailedResult.passed ? '#15803d' : '#991b1b',
                                    marginBottom: '8px'
                                }}>
                                    {detailedResult.passed ? '✓ PASSED' : '✕ NEEDS IMPROVEMENT'}
                                </span>
                                <h3 style={{ margin: '0 0 6px 0', color: '#0f172a' }}>
                                    {detailedResult.assessment_title} — Performance Results
                                </h3>
                                <p style={{ margin: 0, color: '#475569', fontSize: '14px' }}>
                                    Final Score: <strong>{detailedResult.score} / {detailedResult.total_marks}</strong> ({detailedResult.percentage}%)
                                </p>
                            </div>
                            <button
                                onClick={handleExitAttempt}
                                style={{ padding: '9px 18px', backgroundColor: '#0066cc', color: 'white', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', fontSize: '13px' }}
                            >
                                Back to All Assessments
                            </button>
                        </div>

                        {/* Breakdown Metrics */}
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '12px', marginTop: '20px' }}>
                            <div style={{ padding: '10px 14px', backgroundColor: '#ffffff', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                                <div style={{ fontSize: '11px', color: '#64748b', fontWeight: 'bold', textTransform: 'uppercase' }}>Total Questions</div>
                                <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#0f172a', marginTop: '2px' }}>{detailedResult.summary.total_questions}</div>
                            </div>
                            <div style={{ padding: '10px 14px', backgroundColor: '#ffffff', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                                <div style={{ fontSize: '11px', color: '#166534', fontWeight: 'bold', textTransform: 'uppercase' }}>Correct Answers</div>
                                <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#15803d', marginTop: '2px' }}>{detailedResult.summary.correct_count}</div>
                            </div>
                            <div style={{ padding: '10px 14px', backgroundColor: '#ffffff', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                                <div style={{ fontSize: '11px', color: '#991b1b', fontWeight: 'bold', textTransform: 'uppercase' }}>Incorrect Answers</div>
                                <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#dc2626', marginTop: '2px' }}>{detailedResult.summary.incorrect_count}</div>
                            </div>
                            <div style={{ padding: '10px 14px', backgroundColor: '#ffffff', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                                <div style={{ fontSize: '11px', color: '#92400e', fontWeight: 'bold', textTransform: 'uppercase' }}>Unanswered</div>
                                <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#d97706', marginTop: '2px' }}>{detailedResult.summary.unanswered_count}</div>
                            </div>
                        </div>
                    </div>

                    {/* Question Breakdown Filter & List */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
                            <h4 style={{ margin: 0, color: '#1e293b', fontSize: '16px' }}>
                                Question Analysis & Mistake Log
                            </h4>
                            <div style={{ display: 'flex', gap: '8px' }}>
                                <button
                                    onClick={() => setResultFilter('ALL')}
                                    style={{
                                        padding: '6px 12px',
                                        borderRadius: '4px',
                                        fontSize: '12px',
                                        fontWeight: 'bold',
                                        border: '1px solid #cbd5e1',
                                        backgroundColor: resultFilter === 'ALL' ? '#0066cc' : '#ffffff',
                                        color: resultFilter === 'ALL' ? '#ffffff' : '#334155',
                                        cursor: 'pointer'
                                    }}
                                >
                                    All ({detailedResult.questions.length})
                                </button>
                                <button
                                    onClick={() => setResultFilter('MISTAKES')}
                                    style={{
                                        padding: '6px 12px',
                                        borderRadius: '4px',
                                        fontSize: '12px',
                                        fontWeight: 'bold',
                                        border: '1px solid #fecaca',
                                        backgroundColor: resultFilter === 'MISTAKES' ? '#dc2626' : '#fff5f5',
                                        color: resultFilter === 'MISTAKES' ? '#ffffff' : '#991b1b',
                                        cursor: 'pointer'
                                    }}
                                >
                                    Mistakes & Unanswered ({detailedResult.summary.incorrect_count + detailedResult.summary.unanswered_count})
                                </button>
                                <button
                                    onClick={() => setResultFilter('CORRECT')}
                                    style={{
                                        padding: '6px 12px',
                                        borderRadius: '4px',
                                        fontSize: '12px',
                                        fontWeight: 'bold',
                                        border: '1px solid #bbf7d0',
                                        backgroundColor: resultFilter === 'CORRECT' ? '#16a34a' : '#f0fdf4',
                                        color: resultFilter === 'CORRECT' ? '#ffffff' : '#15803d',
                                        cursor: 'pointer'
                                    }}
                                >
                                    Correct ({detailedResult.summary.correct_count})
                                </button>
                            </div>
                        </div>

                        {/* Questions List */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                            {filteredQuestions.map((q) => {
                                const isMistake = !q.is_correct;
                                const isUnanswered = !q.selected_answer;
                                const diff = DIFFICULTY_COLORS[q.difficulty] || DIFFICULTY_COLORS.MEDIUM;

                                return (
                                    <div
                                        key={q.question_id}
                                        style={{
                                            padding: '18px 20px',
                                            backgroundColor: '#ffffff',
                                            borderRadius: '8px',
                                            border: `1px solid ${q.is_correct ? '#bbf7d0' : '#fecaca'}`,
                                            boxShadow: '0 1px 3px rgba(0,0,0,0.04)'
                                        }}
                                    >
                                        {/* Question Card Header */}
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '10px', marginBottom: '10px' }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                                                <span style={{ fontSize: '13px', fontWeight: 'bold', color: '#0f172a' }}>
                                                    Q{q.question_number}.
                                                </span>
                                                <span style={{ fontSize: '11px', fontWeight: 'bold', padding: '2px 8px', borderRadius: '4px', backgroundColor: '#f1f5f9', color: '#334155' }}>
                                                    {q.category} — {q.topic}
                                                </span>
                                                <span style={{ fontSize: '11px', fontWeight: 'bold', padding: '2px 6px', borderRadius: '4px', backgroundColor: diff.bg, color: diff.text }}>
                                                    {q.difficulty}
                                                </span>
                                                <span style={{
                                                    fontSize: '11px',
                                                    fontWeight: 'bold',
                                                    padding: '2px 8px',
                                                    borderRadius: '4px',
                                                    backgroundColor: q.is_correct ? '#dcfce7' : (isUnanswered ? '#fef3c7' : '#fee2e2'),
                                                    color: q.is_correct ? '#15803d' : (isUnanswered ? '#92400e' : '#991b1b')
                                                }}>
                                                    {q.is_correct ? '✓ Correct (+1)' : (isUnanswered ? '⚠️ Unanswered (0)' : '✕ Incorrect (0)')}
                                                </span>
                                            </div>

                                            {/* Weakness Action Button for Mistakes */}
                                            {isMistake && (
                                                <div>
                                                    {q.is_in_weaknesses ? (
                                                        <span style={{
                                                            fontSize: '12px',
                                                            fontWeight: 'bold',
                                                            padding: '4px 10px',
                                                            borderRadius: '4px',
                                                            backgroundColor: '#dcfce7',
                                                            color: '#166534',
                                                            border: '1px solid #86efac',
                                                            display: 'inline-flex',
                                                            alignItems: 'center',
                                                            gap: '4px'
                                                        }}>
                                                            ✓ Added to Weaknesses
                                                        </span>
                                                    ) : (
                                                        <button
                                                            onClick={() => handleAddToWeaknesses(q)}
                                                            disabled={addingWeaknessId === q.question_id}
                                                            style={{
                                                                padding: '5px 12px',
                                                                backgroundColor: '#ef4444',
                                                                color: 'white',
                                                                border: 'none',
                                                                borderRadius: '4px',
                                                                fontSize: '12px',
                                                                fontWeight: 'bold',
                                                                cursor: 'pointer'
                                                            }}
                                                        >
                                                            {addingWeaknessId === q.question_id ? 'Adding...' : '+ Add to Weaknesses'}
                                                        </button>
                                                    )}
                                                </div>
                                            )}
                                        </div>

                                        {/* Prompt */}
                                        <div style={{ fontSize: '15px', fontWeight: '600', color: '#1e293b', marginBottom: '12px' }}>
                                            {q.question}
                                        </div>

                                        {/* Options Breakdown */}
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '12px' }}>
                                            {q.options.map((opt, optIdx) => {
                                                const isCorrectOption = (opt.trim().toLowerCase() === q.correct_answer.trim().toLowerCase());
                                                const isUserSelected = (q.selected_answer && opt.trim().toLowerCase() === q.selected_answer.trim().toLowerCase());

                                                let bg = '#f8fafc';
                                                let border = '#e2e8f0';
                                                let badge = null;

                                                if (isCorrectOption && isUserSelected) {
                                                    bg = '#dcfce7';
                                                    border = '#86efac';
                                                    badge = <span style={{ color: '#15803d', fontWeight: 'bold', fontSize: '11px' }}>(Your Answer — Correct ✓)</span>;
                                                } else if (isCorrectOption) {
                                                    bg = '#f0fdf4';
                                                    border = '#bbf7d0';
                                                    badge = <span style={{ color: '#16a34a', fontWeight: 'bold', fontSize: '11px' }}>(Correct Answer ✓)</span>;
                                                } else if (isUserSelected) {
                                                    bg = '#fee2e2';
                                                    border = '#fca5a5';
                                                    badge = <span style={{ color: '#dc2626', fontWeight: 'bold', fontSize: '11px' }}>(Your Answer — Incorrect ✕)</span>;
                                                }

                                                return (
                                                    <div
                                                        key={optIdx}
                                                        style={{
                                                            padding: '8px 12px',
                                                            borderRadius: '4px',
                                                            backgroundColor: bg,
                                                            border: `1px solid ${border}`,
                                                            fontSize: '13px',
                                                            color: '#334155',
                                                            display: 'flex',
                                                            justifyContent: 'space-between',
                                                            alignItems: 'center'
                                                        }}
                                                    >
                                                        <span>{opt}</span>
                                                        {badge}
                                                    </div>
                                                );
                                            })}
                                        </div>

                                        {/* Explanation Box */}
                                        <div style={{ padding: '10px 14px', backgroundColor: '#f1f5f9', borderRadius: '6px', borderLeft: '3px solid #0066cc', fontSize: '13px', color: '#334155' }}>
                                            <strong style={{ color: '#0f172a' }}>Explanation: </strong>
                                            {q.explanation}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </div>
            )}

            {/* AVAILABLE ASSESSMENTS SECTION */}
            {!activeAttempt && !detailedResult && (
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
            {!activeAttempt && !detailedResult && (
                <div style={{ padding: '25px', backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                    <h3 style={{ margin: '0 0 15px 0', color: '#1e293b' }}>Previous Attempts & Results</h3>
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
                                        <th style={{ padding: '10px', textAlign: 'right' }}>Actions</th>
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
                                            <td style={{ padding: '12px 10px', textAlign: 'right' }}>
                                                {att.status === 'SUBMITTED' && (
                                                    <button
                                                        onClick={() => handleViewResult(att.attempt_id)}
                                                        style={{
                                                            padding: '5px 10px',
                                                            backgroundColor: '#f1f5f9',
                                                            border: '1px solid #cbd5e1',
                                                            borderRadius: '4px',
                                                            fontSize: '12px',
                                                            color: '#0066cc',
                                                            fontWeight: 'bold',
                                                            cursor: 'pointer'
                                                        }}
                                                    >
                                                        Review Mistakes →
                                                    </button>
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

