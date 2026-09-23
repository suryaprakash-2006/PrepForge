import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    getCodingAssessments,
    getUserCodingAttempts,
    getCodingAssessment,
    startCodingAttempt,
    submitCodingProblem,
    submitCodingAttempt,
    getCodingAttempt
} from '../services/api';

const DIFFICULTY_BADGES = {
    EASY: { bg: '#ecfdf5', text: '#059669', border: '#a7f3d0' },
    MEDIUM: { bg: '#fffbeb', text: '#d97706', border: '#fde68a' },
    HARD: { bg: '#fef2f2', text: '#dc2626', border: '#fecaca' }
};

const CodingAssessments = () => {
    const navigate = useNavigate();
    const [assessments, setAssessments] = useState([]);
    const [attempts, setAttempts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Active Attempt State
    const [activeAttempt, setActiveAttempt] = useState(null);
    const [problems, setProblems] = useState([]);
    const [activeProblemIndex, setActiveProblemIndex] = useState(0);
    const [codeState, setCodeState] = useState({}); // { [problemId]: { code: string, language: string, status: string } }
    const [savingProblemId, setSavingProblemId] = useState(null);
    const [submittingAssessment, setSubmittingAssessment] = useState(false);
    const [showSubmitModal, setShowSubmitModal] = useState(false);
    const [timeRemaining, setTimeRemaining] = useState(null);

    // Submitted View State
    const [reviewAttempt, setReviewAttempt] = useState(null);
    const [reviewProblems, setReviewProblems] = useState([]);
    const [reviewProblemIndex, setReviewProblemIndex] = useState(0);

    const fetchData = async () => {
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const [assList, attList] = await Promise.all([
                getCodingAssessments(token),
                getUserCodingAttempts(token)
            ]);
            setAssessments(assList);
            setAttempts(attList);
        } catch (err) {
            setError(err.message || 'Failed to load coding assessments data');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    // Timer countdown effect for active attempt
    useEffect(() => {
        if (!activeAttempt || activeAttempt.status !== 'IN_PROGRESS') {
            setTimeRemaining(null);
            return;
        }

        const startedAtMs = new Date(activeAttempt.started_at).getTime();
        const durationMs = (activeAttempt.duration_minutes || 60) * 60 * 1000;
        const endTime = startedAtMs + durationMs;

        const updateTimer = () => {
            const now = Date.now();
            const diff = Math.max(0, endTime - now);
            setTimeRemaining(diff);
        };

        updateTimer();
        const interval = setInterval(updateTimer, 1000);
        return () => clearInterval(interval);
    }, [activeAttempt]);

    const formatTimer = (ms) => {
        if (ms === null || ms === undefined) return '--:--';
        const totalSeconds = Math.floor(ms / 1000);
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    };

    const handleStartAssessment = async (assessmentId) => {
        setError('');
        setLoading(true);
        try {
            const token = localStorage.getItem('token');
            const data = await startCodingAttempt(token, assessmentId);
            setActiveAttempt(data);
            setProblems(data.problems || []);
            setActiveProblemIndex(0);

            // Populate initial code state
            const initialMap = {};
            (data.problems || []).forEach(p => {
                const state = (data.problem_states || []).find(ps => ps.problem_id === p.id);
                initialMap[p.id] = {
                    code: state ? state.code : (p.starter_code?.python || ''),
                    language: state?.language || 'python',
                    submission_status: state?.submission_status || 'NOT_SUBMITTED'
                };
            });
            setCodeState(initialMap);
            setReviewAttempt(null);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (err) {
            setError(err.message || 'Failed to start coding assessment');
        } finally {
            setLoading(false);
        }
    };

    const handleCodeChange = (problemId, newCode) => {
        setCodeState(prev => ({
            ...prev,
            [problemId]: {
                ...prev[problemId],
                code: newCode
            }
        }));
    };

    const handleLanguageChange = (problemId, newLang) => {
        const currentProblem = problems.find(p => p.id === problemId);
        const starter = currentProblem?.starter_code?.[newLang] || '';
        
        setCodeState(prev => {
            const currentCode = prev[problemId]?.code || '';
            // If empty or matches previous starter, swap to new starter
            const previousStarter = currentProblem?.starter_code?.[prev[problemId]?.language];
            const useStarter = !currentCode || currentCode === previousStarter;

            return {
                ...prev,
                [problemId]: {
                    ...prev[problemId],
                    language: newLang,
                    code: useStarter ? starter : currentCode
                }
            };
        });
    };

    const handleSaveProblemCode = async (problemId) => {
        if (!activeAttempt) return;
        const currentProblemState = codeState[problemId];
        if (!currentProblemState) return;

        setSavingProblemId(problemId);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const res = await submitCodingProblem(
                token,
                activeAttempt.attempt_id,
                problemId,
                currentProblemState.code,
                currentProblemState.language
            );

            setCodeState(prev => ({
                ...prev,
                [problemId]: {
                    ...prev[problemId],
                    submission_status: 'SUBMITTED'
                }
            }));
        } catch (err) {
            setError(err.message || 'Failed to save problem solution');
        } finally {
            setSavingProblemId(null);
        }
    };

    const handleFinalSubmit = async () => {
        if (!activeAttempt) return;
        setSubmittingAssessment(true);
        setError('');
        try {
            const token = localStorage.getItem('token');

            // Save active problem first if modified
            const activeProblem = problems[activeProblemIndex];
            if (activeProblem && codeState[activeProblem.id]) {
                try {
                    await submitCodingProblem(
                        token,
                        activeAttempt.attempt_id,
                        activeProblem.id,
                        codeState[activeProblem.id].code,
                        codeState[activeProblem.id].language
                    );
                } catch (e) {
                    console.error('Auto-save on submit failed', e);
                }
            }

            await submitCodingAttempt(token, activeAttempt.attempt_id);
            setShowSubmitModal(false);
            
            // Switch to review view for this attempt
            await handleViewAttempt(activeAttempt.attempt_id, activeAttempt.assessment_id);
            setActiveAttempt(null);
            fetchData();
        } catch (err) {
            setError(err.message || 'Failed to submit coding assessment');
        } finally {
            setSubmittingAssessment(false);
        }
    };

    const handleViewAttempt = async (attemptId, assessmentId) => {
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const [attemptDoc, assessmentDetail] = await Promise.all([
                getCodingAttempt(token, attemptId),
                getCodingAssessment(token, assessmentId)
            ]);

            setReviewAttempt(attemptDoc);
            setReviewProblems(assessmentDetail.problems || []);
            setReviewProblemIndex(0);
            setActiveAttempt(null);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (err) {
            setError(err.message || 'Failed to load attempt details');
        } finally {
            setLoading(false);
        }
    };

    // Textarea Tab key support
    const handleKeyDown = (e, problemId) => {
        if (e.key === 'Tab') {
            e.preventDefault();
            const target = e.target;
            const start = target.selectionStart;
            const end = target.selectionEnd;
            const val = target.value;
            const newVal = val.substring(0, start) + '    ' + val.substring(end);
            handleCodeChange(problemId, newVal);
            setTimeout(() => {
                target.selectionStart = target.selectionEnd = start + 4;
            }, 0);
        }
    };

    const currentProblem = problems[activeProblemIndex];
    const currentReviewProblem = reviewProblems[reviewProblemIndex];

    return (
        <div style={{ padding: '2rem 1.5rem', maxWidth: '1400px', margin: '0 auto', fontFamily: 'Inter, system-ui, sans-serif' }}>
            {/* Header */}
            <div style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                <div>
                    <h1 style={{ fontSize: '1.875rem', fontWeight: '800', color: '#0f172a', margin: '0 0 0.5rem 0' }}>
                        Timed Coding Assessments
                    </h1>
                    <p style={{ color: '#64748b', margin: 0, fontSize: '0.95rem' }}>
                        Week 11 Intensive Simulation Engine — Curated DSA problem sets with real interview time constraints.
                    </p>
                </div>
                {(activeAttempt || reviewAttempt) && (
                    <button
                        onClick={() => {
                            setActiveAttempt(null);
                            setReviewAttempt(null);
                        }}
                        style={{
                            background: '#f1f5f9',
                            color: '#334155',
                            border: '1px solid #cbd5e1',
                            padding: '0.5rem 1rem',
                            borderRadius: '8px',
                            fontWeight: '600',
                            fontSize: '0.875rem',
                            cursor: 'pointer'
                        }}
                    >
                        ← Back to Assessments List
                    </button>
                )}
            </div>

            {error && (
                <div style={{
                    background: '#fef2f2',
                    border: '1px solid #fecaca',
                    color: '#991b1b',
                    padding: '1rem',
                    borderRadius: '8px',
                    marginBottom: '1.5rem',
                    fontSize: '0.9rem'
                }}>
                    <strong>Error:</strong> {error}
                </div>
            )}

            {/* 1. ACTIVE ASSESSMENT TEST RUNNER */}
            {activeAttempt && currentProblem && (
                <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
                    {/* Test Runner Top Bar */}
                    <div style={{
                        background: '#0f172a',
                        color: '#f8fafc',
                        padding: '1rem 1.5rem',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        flexWrap: 'wrap',
                        gap: '1rem'
                    }}>
                        <div>
                            <span style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8' }}>
                                Active Simulation Attempt
                            </span>
                            <h2 style={{ fontSize: '1.25rem', fontWeight: '700', margin: '0.25rem 0 0 0', color: '#ffffff' }}>
                                {activeAttempt.assessment_title || 'Week 11 Coding Assessment'}
                            </h2>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                            <div style={{
                                background: timeRemaining !== null && timeRemaining < 300000 ? '#7f1d1d' : '#1e293b',
                                border: '1px solid #334155',
                                padding: '0.5rem 1rem',
                                borderRadius: '8px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.5rem'
                            }}>
                                <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Time Remaining:</span>
                                <span style={{ fontSize: '1.125rem', fontWeight: '800', fontFamily: 'monospace', color: timeRemaining !== null && timeRemaining < 300000 ? '#fca5a5' : '#38bdf8' }}>
                                    {formatTimer(timeRemaining)}
                                </span>
                            </div>

                            <button
                                onClick={() => setShowSubmitModal(true)}
                                style={{
                                    background: '#2563eb',
                                    color: '#ffffff',
                                    border: 'none',
                                    padding: '0.625rem 1.25rem',
                                    borderRadius: '8px',
                                    fontWeight: '700',
                                    fontSize: '0.9rem',
                                    cursor: 'pointer',
                                    transition: 'background 0.2s'
                                }}
                            >
                                Finish & Submit Assessment
                            </button>
                        </div>
                    </div>

                    {/* Problem Navigation Tabs */}
                    <div style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', display: 'flex', padding: '0.5rem 1rem 0', gap: '0.5rem' }}>
                        {problems.map((p, idx) => {
                            const isSubmitted = codeState[p.id]?.submission_status === 'SUBMITTED';
                            const isActive = idx === activeProblemIndex;
                            return (
                                <button
                                    key={p.id}
                                    onClick={() => setActiveProblemIndex(idx)}
                                    style={{
                                        padding: '0.625rem 1rem',
                                        borderTopLeftRadius: '8px',
                                        borderTopRightRadius: '8px',
                                        border: isActive ? '1px solid #e2e8f0' : '1px solid transparent',
                                        borderBottom: isActive ? '2px solid #2563eb' : 'none',
                                        background: isActive ? '#ffffff' : 'transparent',
                                        color: isActive ? '#0f172a' : '#64748b',
                                        fontWeight: isActive ? '700' : '500',
                                        fontSize: '0.875rem',
                                        cursor: 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '0.5rem'
                                    }}
                                >
                                    <span>Problem {idx + 1}</span>
                                    <span style={{
                                        width: '8px',
                                        height: '8px',
                                        borderRadius: '50%',
                                        background: isSubmitted ? '#10b981' : '#cbd5e1'
                                    }} title={isSubmitted ? 'Solution Saved' : 'Not Saved'} />
                                </button>
                            );
                        })}
                    </div>

                    {/* Split View Editor */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'minmax(380px, 1fr) minmax(480px, 1.2fr)', minHeight: '680px' }}>
                        {/* Problem Description Panel */}
                        <div style={{ padding: '1.5rem', borderRight: '1px solid #e2e8f0', overflowY: 'auto', maxHeight: '720px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                                <span style={{
                                    fontSize: '0.75rem',
                                    fontWeight: '700',
                                    padding: '0.2rem 0.6rem',
                                    borderRadius: '9999px',
                                    background: DIFFICULTY_BADGES[currentProblem.difficulty]?.bg || '#f1f5f9',
                                    color: DIFFICULTY_BADGES[currentProblem.difficulty]?.text || '#334155',
                                    border: `1px solid ${DIFFICULTY_BADGES[currentProblem.difficulty]?.border || '#cbd5e1'}`
                                }}>
                                    {currentProblem.difficulty}
                                </span>
                                <span style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: '500' }}>
                                    {currentProblem.category} • {currentProblem.topic}
                                </span>
                            </div>

                            <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#0f172a', margin: '0 0 1rem 0' }}>
                                {currentProblem.title}
                            </h3>

                            <div style={{ color: '#334155', fontSize: '0.95rem', lineHeight: '1.6', marginBottom: '1.5rem' }}>
                                {currentProblem.description}
                            </div>

                            {/* Examples */}
                            <h4 style={{ fontSize: '0.9rem', fontWeight: '700', color: '#0f172a', marginBottom: '0.5rem' }}>Examples</h4>
                            {currentProblem.examples && currentProblem.examples.map((ex, i) => (
                                <div key={i} style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '0.75rem 1rem', marginBottom: '0.75rem', fontSize: '0.875rem' }}>
                                    <div style={{ marginBottom: '0.25rem' }}>
                                        <strong style={{ color: '#475569' }}>Input: </strong>
                                        <code style={{ color: '#0f172a', fontFamily: 'monospace' }}>{ex.input}</code>
                                    </div>
                                    <div style={{ marginBottom: '0.25rem' }}>
                                        <strong style={{ color: '#475569' }}>Output: </strong>
                                        <code style={{ color: '#0f172a', fontFamily: 'monospace' }}>{ex.output}</code>
                                    </div>
                                    {ex.explanation && (
                                        <div style={{ color: '#64748b', fontSize: '0.8rem', marginTop: '0.25rem' }}>
                                            <em>Explanation:</em> {ex.explanation}
                                        </div>
                                    )}
                                </div>
                            ))}

                            {/* Constraints */}
                            {currentProblem.constraints && currentProblem.constraints.length > 0 && (
                                <div style={{ marginTop: '1.5rem' }}>
                                    <h4 style={{ fontSize: '0.9rem', fontWeight: '700', color: '#0f172a', marginBottom: '0.5rem' }}>Constraints</h4>
                                    <ul style={{ margin: 0, paddingLeft: '1.25rem', color: '#475569', fontSize: '0.875rem', lineHeight: '1.5' }}>
                                        {currentProblem.constraints.map((c, i) => (
                                            <li key={i}><code style={{ fontFamily: 'monospace' }}>{c}</code></li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Tags */}
                            {currentProblem.tags && (
                                <div style={{ marginTop: '1.5rem', display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                                    {currentProblem.tags.map((t, i) => (
                                        <span key={i} style={{ background: '#f1f5f9', color: '#475569', fontSize: '0.75rem', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
                                            #{t}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>

                        {/* Code Editor Panel */}
                        <div style={{ display: 'flex', flexDirection: 'column', background: '#090d16', color: '#f8fafc' }}>
                            {/* Editor Top Bar */}
                            <div style={{ padding: '0.75rem 1.25rem', background: '#111827', borderBottom: '1px solid #1f2937', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                    <label style={{ fontSize: '0.8rem', color: '#9ca3af' }}>Language:</label>
                                    <select
                                        value={codeState[currentProblem.id]?.language || 'python'}
                                        onChange={(e) => handleLanguageChange(currentProblem.id, e.target.value)}
                                        style={{
                                            background: '#1f2937',
                                            color: '#f9fafb',
                                            border: '1px solid #374151',
                                            padding: '0.35rem 0.75rem',
                                            borderRadius: '6px',
                                            fontSize: '0.85rem',
                                            cursor: 'pointer'
                                        }}
                                    >
                                        <option value="python">Python 3</option>
                                        <option value="cpp">C++ 20</option>
                                    </select>
                                </div>

                                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                    <span style={{
                                        fontSize: '0.75rem',
                                        fontWeight: '600',
                                        color: codeState[currentProblem.id]?.submission_status === 'SUBMITTED' ? '#34d399' : '#9ca3af',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '0.4rem'
                                    }}>
                                        <span style={{
                                            width: '6px',
                                            height: '6px',
                                            borderRadius: '50%',
                                            background: codeState[currentProblem.id]?.submission_status === 'SUBMITTED' ? '#34d399' : '#6b7280'
                                        }} />
                                        {codeState[currentProblem.id]?.submission_status === 'SUBMITTED' ? 'Saved & Marked' : 'Unsaved Draft'}
                                    </span>

                                    <button
                                        onClick={() => handleSaveProblemCode(currentProblem.id)}
                                        disabled={savingProblemId === currentProblem.id}
                                        style={{
                                            background: '#10b981',
                                            color: '#ffffff',
                                            border: 'none',
                                            padding: '0.4rem 0.9rem',
                                            borderRadius: '6px',
                                            fontWeight: '600',
                                            fontSize: '0.825rem',
                                            cursor: savingProblemId === currentProblem.id ? 'not-allowed' : 'pointer',
                                            opacity: savingProblemId === currentProblem.id ? 0.7 : 1
                                        }}
                                    >
                                        {savingProblemId === currentProblem.id ? 'Saving...' : 'Save Solution'}
                                    </button>
                                </div>
                            </div>

                            {/* Code Textarea Area */}
                            <div style={{ flex: 1, padding: '1rem', display: 'flex', flexDirection: 'column' }}>
                                <textarea
                                    value={codeState[currentProblem.id]?.code || ''}
                                    onChange={(e) => handleCodeChange(currentProblem.id, e.target.value)}
                                    onKeyDown={(e) => handleKeyDown(e, currentProblem.id)}
                                    placeholder="// Write your solution code here..."
                                    spellCheck={false}
                                    style={{
                                        flex: 1,
                                        width: '100%',
                                        minHeight: '480px',
                                        background: '#090d16',
                                        color: '#f8fafc',
                                        border: 'none',
                                        outline: 'none',
                                        resize: 'none',
                                        fontFamily: 'Consolas, Menlo, Monaco, "Courier New", monospace',
                                        fontSize: '0.95rem',
                                        lineHeight: '1.6',
                                        tabSize: 4
                                    }}
                                />
                            </div>

                            {/* Editor Invariant Note */}
                            <div style={{ padding: '0.5rem 1.25rem', background: '#111827', borderTop: '1px solid #1f2937', color: '#6b7280', fontSize: '0.75rem', display: 'flex', justifyContent: 'space-between' }}>
                                <span>PrepForge Assessment Engine Foundation</span>
                                <span>Code is saved as plain text (Max 64KB)</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* 2. SUBMITTED ATTEMPT REVIEW SCREEN */}
            {reviewAttempt && currentReviewProblem && (
                <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
                    {/* Top Review Bar */}
                    <div style={{ background: '#0f172a', color: '#ffffff', padding: '1.25rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                        <div>
                            <span style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#38bdf8' }}>
                                Attempt Review Mode (Submitted)
                            </span>
                            <h2 style={{ fontSize: '1.25rem', fontWeight: '700', margin: '0.25rem 0 0 0' }}>
                                {reviewAttempt.assessment_title || 'Coding Assessment'}
                            </h2>
                        </div>
                        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                            <span style={{ background: '#10b981', color: '#ffffff', padding: '0.35rem 0.85rem', borderRadius: '9999px', fontSize: '0.8rem', fontWeight: '700' }}>
                                SUBMITTED
                            </span>
                            <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
                                Submitted: {new Date(reviewAttempt.submitted_at).toLocaleString()}
                            </span>
                        </div>
                    </div>

                    {/* Informational Callout */}
                    <div style={{ background: '#f0fdf4', borderBottom: '1px solid #bbf7d0', padding: '1rem 1.5rem', color: '#166534', fontSize: '0.875rem' }}>
                        <strong>Submission Stored:</strong> Your code submissions have been recorded and locked for evaluation. No code execution sandbox or automated test runner was run during this foundation stage.
                    </div>

                    {/* Navigation Tabs */}
                    <div style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', display: 'flex', padding: '0.5rem 1rem 0', gap: '0.5rem' }}>
                        {reviewProblems.map((p, idx) => {
                            const state = (reviewAttempt.problem_states || []).find(ps => ps.problem_id === p.id);
                            const isSubmitted = state?.submission_status === 'SUBMITTED';
                            const isActive = idx === reviewProblemIndex;
                            return (
                                <button
                                    key={p.id}
                                    onClick={() => setReviewProblemIndex(idx)}
                                    style={{
                                        padding: '0.625rem 1rem',
                                        borderTopLeftRadius: '8px',
                                        borderTopRightRadius: '8px',
                                        border: isActive ? '1px solid #e2e8f0' : '1px solid transparent',
                                        borderBottom: isActive ? '2px solid #2563eb' : 'none',
                                        background: isActive ? '#ffffff' : 'transparent',
                                        color: isActive ? '#0f172a' : '#64748b',
                                        fontWeight: isActive ? '700' : '500',
                                        fontSize: '0.875rem',
                                        cursor: 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '0.5rem'
                                    }}
                                >
                                    <span>Problem {idx + 1}: {p.title}</span>
                                    <span style={{
                                        width: '8px',
                                        height: '8px',
                                        borderRadius: '50%',
                                        background: isSubmitted ? '#10b981' : '#cbd5e1'
                                    }} />
                                </button>
                            );
                        })}
                    </div>

                    {/* Split View for Review */}
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', minHeight: '550px' }}>
                        <div style={{ padding: '1.5rem', borderRight: '1px solid #e2e8f0', overflowY: 'auto', maxHeight: '600px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                                <span style={{
                                    fontSize: '0.75rem',
                                    fontWeight: '700',
                                    padding: '0.2rem 0.6rem',
                                    borderRadius: '9999px',
                                    background: DIFFICULTY_BADGES[currentReviewProblem.difficulty]?.bg,
                                    color: DIFFICULTY_BADGES[currentReviewProblem.difficulty]?.text
                                }}>
                                    {currentReviewProblem.difficulty}
                                </span>
                                <span style={{ fontSize: '0.8rem', color: '#64748b' }}>
                                    {currentReviewProblem.category} • {currentReviewProblem.topic}
                                </span>
                            </div>

                            <h3 style={{ fontSize: '1.2rem', fontWeight: '800', color: '#0f172a', margin: '0 0 1rem 0' }}>
                                {currentReviewProblem.title}
                            </h3>

                            <div style={{ color: '#334155', fontSize: '0.9rem', lineHeight: '1.6', marginBottom: '1rem' }}>
                                {currentReviewProblem.description}
                            </div>
                        </div>

                        {/* Read-only Code Box */}
                        {(() => {
                            const pState = (reviewAttempt.problem_states || []).find(ps => ps.problem_id === currentReviewProblem.id);
                            return (
                                <div style={{ background: '#090d16', color: '#f8fafc', padding: '1.25rem', display: 'flex', flexDirection: 'column' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem', color: '#9ca3af', fontSize: '0.8rem' }}>
                                        <span>Language: <strong>{pState?.language || 'python'}</strong></span>
                                        <span>Status: <strong style={{ color: pState?.submission_status === 'SUBMITTED' ? '#34d399' : '#f87171' }}>{pState?.submission_status || 'NOT_SUBMITTED'}</strong></span>
                                    </div>
                                    <pre style={{
                                        flex: 1,
                                        margin: 0,
                                        background: '#111827',
                                        padding: '1rem',
                                        borderRadius: '8px',
                                        overflowX: 'auto',
                                        fontFamily: 'Consolas, Menlo, Monaco, monospace',
                                        fontSize: '0.9rem',
                                        color: '#e2e8f0',
                                        lineHeight: '1.5'
                                    }}>
                                        {pState?.code || '// No code submitted for this problem'}
                                    </pre>
                                </div>
                            );
                        })()}
                    </div>
                </div>
            )}

            {/* 3. ASSESSMENTS LIST & HISTORY (Shown when not taking/reviewing an attempt) */}
            {!activeAttempt && !reviewAttempt && (
                <div>
                    {/* Assessment Cards Grid */}
                    <h2 style={{ fontSize: '1.25rem', fontWeight: '700', color: '#0f172a', marginBottom: '1rem' }}>
                        Available Simulations
                    </h2>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
                        {assessments.map(ass => (
                            <div
                                key={ass.id}
                                style={{
                                    background: '#ffffff',
                                    border: '1px solid #e2e8f0',
                                    borderRadius: '12px',
                                    padding: '1.5rem',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    justifyContent: 'space-between',
                                    boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                                    transition: 'transform 0.15s, box-shadow 0.15s'
                                }}
                            >
                                <div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                                        <span style={{
                                            background: '#fef3c7',
                                            color: '#92400e',
                                            border: '1px solid #fde68a',
                                            fontSize: '0.75rem',
                                            fontWeight: '700',
                                            padding: '0.2rem 0.6rem',
                                            borderRadius: '9999px'
                                        }}>
                                            WEEK {ass.week_number} TIMED CODING
                                        </span>
                                        <span style={{ fontSize: '0.85rem', color: '#64748b', fontWeight: '600' }}>
                                            ⏱ {ass.duration_minutes} mins
                                        </span>
                                    </div>

                                    <h3 style={{ fontSize: '1.15rem', fontWeight: '800', color: '#0f172a', margin: '0 0 0.5rem 0' }}>
                                        {ass.title}
                                    </h3>

                                    <p style={{ color: '#64748b', fontSize: '0.875rem', lineHeight: '1.5', margin: '0 0 1.25rem 0' }}>
                                        {ass.description}
                                    </p>

                                    <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.8rem', color: '#475569', marginBottom: '1.5rem' }}>
                                        <div><strong>Problems:</strong> {ass.problem_count} Algorithmic Tasks</div>
                                        <div><strong>Target:</strong> {ass.passing_score}% Completion</div>
                                    </div>
                                </div>

                                <button
                                    onClick={() => handleStartAssessment(ass.id)}
                                    style={{
                                        width: '100%',
                                        background: '#2563eb',
                                        color: '#ffffff',
                                        border: 'none',
                                        padding: '0.75rem',
                                        borderRadius: '8px',
                                        fontWeight: '700',
                                        fontSize: '0.9rem',
                                        cursor: 'pointer'
                                    }}
                                >
                                    Start Simulation Attempt →
                                </button>
                            </div>
                        ))}
                    </div>

                    {/* Attempt History Table */}
                    <h2 style={{ fontSize: '1.25rem', fontWeight: '700', color: '#0f172a', marginBottom: '1rem' }}>
                        Attempt History
                    </h2>
                    {attempts.length === 0 ? (
                        <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '2.5rem', textAlign: 'center', color: '#64748b' }}>
                            <p style={{ margin: 0, fontSize: '0.95rem' }}>No coding assessment attempts recorded yet. Start a simulation above to begin tracking your coding runs.</p>
                        </div>
                    ) : (
                        <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
                                <thead>
                                    <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', color: '#475569' }}>
                                        <th style={{ padding: '0.875rem 1.25rem', fontWeight: '600' }}>Assessment</th>
                                        <th style={{ padding: '0.875rem 1.25rem', fontWeight: '600' }}>Started</th>
                                        <th style={{ padding: '0.875rem 1.25rem', fontWeight: '600' }}>Status</th>
                                        <th style={{ padding: '0.875rem 1.25rem', fontWeight: '600' }}>Submitted Problems</th>
                                        <th style={{ padding: '0.875rem 1.25rem', fontWeight: '600', textAlign: 'right' }}>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {attempts.map(att => (
                                        <tr key={att.attempt_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                                            <td style={{ padding: '1rem 1.25rem', fontWeight: '600', color: '#0f172a' }}>
                                                {att.assessment_title}
                                            </td>
                                            <td style={{ padding: '1rem 1.25rem', color: '#64748b' }}>
                                                {new Date(att.started_at).toLocaleString()}
                                            </td>
                                            <td style={{ padding: '1rem 1.25rem' }}>
                                                <span style={{
                                                    fontSize: '0.75rem',
                                                    fontWeight: '700',
                                                    padding: '0.2rem 0.6rem',
                                                    borderRadius: '9999px',
                                                    background: att.status === 'SUBMITTED' ? '#ecfdf5' : '#fef3c7',
                                                    color: att.status === 'SUBMITTED' ? '#059669' : '#d97706',
                                                    border: `1px solid ${att.status === 'SUBMITTED' ? '#a7f3d0' : '#fde68a'}`
                                                }}>
                                                    {att.status}
                                                </span>
                                            </td>
                                            <td style={{ padding: '1rem 1.25rem', color: '#334155' }}>
                                                <strong>{att.submitted_problems_count}</strong> / {att.problem_count}
                                            </td>
                                            <td style={{ padding: '1rem 1.25rem', textAlign: 'right' }}>
                                                <button
                                                    onClick={() => handleViewAttempt(att.attempt_id, att.assessment_id)}
                                                    style={{
                                                        background: '#f1f5f9',
                                                        color: '#2563eb',
                                                        border: '1px solid #cbd5e1',
                                                        padding: '0.35rem 0.85rem',
                                                        borderRadius: '6px',
                                                        fontWeight: '600',
                                                        fontSize: '0.8rem',
                                                        cursor: 'pointer'
                                                    }}
                                                >
                                                    {att.status === 'SUBMITTED' ? 'Review Code' : 'View Attempt'}
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}

            {/* Confirmation Modal */}
            {showSubmitModal && (
                <div style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'rgba(15, 23, 42, 0.6)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 9999,
                    padding: '1rem'
                }}>
                    <div style={{ background: '#ffffff', borderRadius: '12px', maxWidth: '480px', width: '100%', padding: '1.75rem', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)' }}>
                        <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#0f172a', margin: '0 0 0.75rem 0' }}>
                            Submit Coding Assessment?
                        </h3>
                        <p style={{ color: '#475569', fontSize: '0.9rem', lineHeight: '1.5', margin: '0 0 1.5rem 0' }}>
                            Once submitted, your assessment attempt will be finalized and all saved solutions will become <strong>immutable</strong>. You will be able to review your submitted code, but cannot edit it further.
                        </p>
                        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
                            <button
                                onClick={() => setShowSubmitModal(false)}
                                style={{
                                    background: '#f1f5f9',
                                    color: '#475569',
                                    border: '1px solid #cbd5e1',
                                    padding: '0.5rem 1rem',
                                    borderRadius: '6px',
                                    fontWeight: '600',
                                    cursor: 'pointer'
                                }}
                            >
                                Continue Working
                            </button>
                            <button
                                onClick={handleFinalSubmit}
                                disabled={submittingAssessment}
                                style={{
                                    background: '#2563eb',
                                    color: '#ffffff',
                                    border: 'none',
                                    padding: '0.5rem 1.25rem',
                                    borderRadius: '6px',
                                    fontWeight: '700',
                                    cursor: submittingAssessment ? 'not-allowed' : 'pointer'
                                }}
                            >
                                {submittingAssessment ? 'Submitting...' : 'Confirm Submission'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CodingAssessments;
