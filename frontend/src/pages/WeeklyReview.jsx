import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { getWeeklyReview, saveWeeklyReview } from '../services/api';

const RATING_LABELS = {
    1: '1 - Low / Struggling',
    2: '2 - Needs Improvement',
    3: '3 - Moderate / On Track',
    4: '4 - Good / Confident',
    5: '5 - Excellent / Mastered'
};

const TagListInput = ({ label, placeholder, tags, onChange, description }) => {
    const [inputValue, setInputValue] = useState('');

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            addItem();
        }
    };

    const addItem = () => {
        const val = inputValue.trim();
        if (val && !tags.includes(val)) {
            onChange([...tags, val]);
            setInputValue('');
        }
    };

    const removeItem = (index) => {
        onChange(tags.filter((_, i) => i !== index));
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <label style={{ fontSize: '13px', fontWeight: 'bold', color: '#334155' }}>
                {label}
            </label>
            {description && (
                <span style={{ fontSize: '12px', color: '#64748b' }}>{description}</span>
            )}
            <div style={{ display: 'flex', gap: '8px' }}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={placeholder}
                    style={{ flex: 1, padding: '8px 12px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px' }}
                />
                <button
                    type="button"
                    onClick={addItem}
                    style={{ padding: '8px 14px', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '4px', cursor: 'pointer', fontSize: '13px', fontWeight: '500' }}
                >
                    Add
                </button>
            </div>
            {tags.length > 0 && (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '4px' }}>
                    {tags.map((tag, idx) => (
                        <span
                            key={idx}
                            style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '6px',
                                padding: '4px 10px',
                                backgroundColor: '#e0f2fe',
                                color: '#0369a1',
                                borderRadius: '16px',
                                fontSize: '13px',
                                border: '1px solid #bae6fd'
                            }}
                        >
                            {tag}
                            <button
                                type="button"
                                onClick={() => removeItem(idx)}
                                style={{ background: 'none', border: 'none', color: '#0284c7', cursor: 'pointer', fontSize: '14px', padding: 0, lineHeight: 1 }}
                            >
                                ×
                            </button>
                        </span>
                    ))}
                </div>
            )}
        </div>
    );
};

const WeeklyReview = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const navigate = useNavigate();

    const currentWeekNum = parseInt(searchParams.get('week') || '1', 10);
    const selectedWeek = isNaN(currentWeekNum) || currentWeekNum < 1 || currentWeekNum > 12 ? 1 : currentWeekNum;

    const [reviewData, setReviewData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');
    const [saveSuccess, setSaveSuccess] = useState(false);

    // Form state
    const [reflectionForm, setReflectionForm] = useState({
        weakest_topics: [],
        improved_topics: [],
        carry_forward_topics: [],
        next_priorities: [],
        confidence: null,
        motivation: null,
        schedule_adjustments: ''
    });

    const fetchReview = async (weekNum) => {
        setLoading(true);
        setError('');
        setSaveSuccess(false);
        try {
            const token = localStorage.getItem('token');
            const data = await getWeeklyReview(token, weekNum);
            setReviewData(data);
            setReflectionForm({
                weakest_topics: data.reflection?.weakest_topics || [],
                improved_topics: data.reflection?.improved_topics || [],
                carry_forward_topics: data.reflection?.carry_forward_topics || [],
                next_priorities: data.reflection?.next_priorities || [],
                confidence: data.reflection?.confidence || null,
                motivation: data.reflection?.motivation || null,
                schedule_adjustments: data.reflection?.schedule_adjustments || ''
            });
        } catch (err) {
            setError(err.message || 'Failed to load weekly review');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchReview(selectedWeek);
    }, [selectedWeek]);

    const handleWeekChange = (wNum) => {
        setSearchParams({ week: wNum.toString() });
    };

    const handleSaveReflection = async (e) => {
        e.preventDefault();
        setSaving(true);
        setError('');
        setSaveSuccess(false);
        try {
            const token = localStorage.getItem('token');
            const updated = await saveWeeklyReview(token, selectedWeek, {
                weakest_topics: reflectionForm.weakest_topics,
                improved_topics: reflectionForm.improved_topics,
                carry_forward_topics: reflectionForm.carry_forward_topics,
                next_priorities: reflectionForm.next_priorities,
                confidence: reflectionForm.confidence,
                motivation: reflectionForm.motivation,
                schedule_adjustments: reflectionForm.schedule_adjustments
            });
            setReviewData(updated);
            setSaveSuccess(true);
            setTimeout(() => setSaveSuccess(false), 4000);
        } catch (err) {
            setError(err.message || 'Failed to save reflection');
        } finally {
            setSaving(false);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #eaeaea', paddingBottom: '15px', flexWrap: 'wrap', gap: '15px' }}>
                <div>
                    <h2 style={{ margin: 0, color: '#1e293b' }}>Weekly Review & Retrospective</h2>
                    <p style={{ margin: '5px 0 0 0', color: '#64748b', fontSize: '14px' }}>
                        Evaluate target completion, synthesize mistake patterns, and plan adjustments for upcoming weeks.
                    </p>
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                        onClick={() => navigate('/app/weaknesses')}
                        style={{ padding: '8px 14px', backgroundColor: '#f1f5f9', color: '#0066cc', border: '1px solid #cbd5e1', borderRadius: '6px', fontSize: '13px', fontWeight: '500', cursor: 'pointer' }}
                    >
                        View All Weaknesses →
                    </button>
                </div>
            </div>

            {/* Week Selector Bar */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', backgroundColor: '#f8fafc', padding: '15px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#475569', textTransform: 'uppercase' }}>
                    Select Week
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {Array.from({ length: 12 }, (_, i) => i + 1).map(w => {
                        const isSelected = w === selectedWeek;
                        return (
                            <button
                                key={w}
                                onClick={() => handleWeekChange(w)}
                                style={{
                                    padding: '8px 14px',
                                    borderRadius: '6px',
                                    border: isSelected ? '2px solid #0066cc' : '1px solid #cbd5e1',
                                    backgroundColor: isSelected ? '#0066cc' : '#ffffff',
                                    color: isSelected ? '#ffffff' : '#334155',
                                    fontWeight: isSelected ? 'bold' : '500',
                                    cursor: 'pointer',
                                    fontSize: '13px',
                                    transition: 'all 0.2s ease'
                                }}
                            >
                                Week {w}
                            </button>
                        );
                    })}
                </div>
            </div>

            {error && (
                <div style={{ padding: '12px 16px', backgroundColor: '#fff5f5', border: '1px solid #fed7d7', borderRadius: '6px', color: '#c53030', fontSize: '14px' }}>
                    {error}
                </div>
            )}

            {loading ? (
                <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>
                    Loading review data for Week {selectedWeek}...
                </div>
            ) : reviewData ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
                    {/* Week Title & Phase Badge */}
                    <div style={{ padding: '18px 20px', backgroundColor: '#f1f5f9', borderRadius: '8px', border: '1px solid #cbd5e1', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
                        <div>
                            <span style={{ fontSize: '12px', fontWeight: 'bold', color: '#0066cc', textTransform: 'uppercase' }}>
                                Week {reviewData.week.week_number} Overview
                            </span>
                            <h3 style={{ margin: '4px 0 0 0', color: '#0f172a' }}>
                                {reviewData.week.title}
                            </h3>
                        </div>
                        {reviewData.week.phase && (
                            <span style={{ padding: '4px 10px', backgroundColor: '#e2e8f0', borderRadius: '12px', fontSize: '12px', fontWeight: 'bold', color: '#475569' }}>
                                {reviewData.week.phase}
                            </span>
                        )}
                    </div>

                    {/* Derived Section 1: Target & Task Completion Summary */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px' }}>
                        {/* Overall Week Completion */}
                        <div style={{ padding: '20px', backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                            <div>
                                <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#64748b', textTransform: 'uppercase' }}>
                                    Week Task Completion
                                </div>
                                <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', marginTop: '10px' }}>
                                    <span style={{ fontSize: '32px', fontWeight: 'bold', color: '#0f172a' }}>
                                        {reviewData.progress.completion_percentage}%
                                    </span>
                                    <span style={{ fontSize: '14px', color: '#64748b' }}>
                                        ({reviewData.progress.completed_tasks} / {reviewData.progress.total_tasks} tasks)
                                    </span>
                                </div>
                            </div>
                            <div style={{ marginTop: '15px' }}>
                                <div style={{ width: '100%', backgroundColor: '#e2e8f0', borderRadius: '4px', height: '8px', overflow: 'hidden' }}>
                                    <div style={{ width: `${reviewData.progress.completion_percentage}%`, backgroundColor: reviewData.progress.completion_percentage === 100 ? '#28a745' : '#0066cc', height: '100%', transition: 'width 0.4s ease' }}></div>
                                </div>
                                <div style={{ fontSize: '12px', color: '#64748b', marginTop: '6px' }}>
                                    {reviewData.progress.remaining_tasks} tasks remaining
                                </div>
                            </div>
                        </div>

                        {/* Weekly Targets Breakdown */}
                        <div style={{ padding: '20px', backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                            <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#64748b', textTransform: 'uppercase', marginBottom: '12px' }}>
                                Practice Targets vs Actuals
                            </div>
                            {Object.keys(reviewData.targets).length === 0 ? (
                                <p style={{ fontSize: '13px', color: '#94a3b8', margin: 0 }}>No explicit practice targets defined for this week.</p>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                                    {Object.entries(reviewData.targets).map(([key, t]) => {
                                        const pct = t.target > 0 ? Math.min(100, Math.round((t.completed / t.target) * 100)) : 0;
                                        const label = key.replace(/_/g, ' ').toUpperCase();
                                        return (
                                            <div key={key}>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
                                                    <span style={{ color: '#334155', fontWeight: '500' }}>{label}</span>
                                                    <strong style={{ color: pct >= 100 ? '#16a34a' : '#0f172a' }}>
                                                        {t.completed} / {t.target} ({pct}%)
                                                    </strong>
                                                </div>
                                                <div style={{ width: '100%', backgroundColor: '#e2e8f0', borderRadius: '3px', height: '6px', overflow: 'hidden' }}>
                                                    <div style={{ width: `${pct}%`, backgroundColor: pct >= 100 ? '#16a34a' : '#0284c7', height: '100%' }}></div>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Derived Section 2: Week Category Breakdown */}
                    <div style={{ padding: '20px', backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                        <h4 style={{ margin: '0 0 12px 0', fontSize: '15px', color: '#1e293b' }}>
                            Week {reviewData.week.week_number} Category Breakdown
                        </h4>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
                            {reviewData.categories.map(cat => (
                                <div key={cat.category} style={{ padding: '10px 14px', backgroundColor: '#f8fafc', borderRadius: '6px', border: '1px solid #f1f5f9' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                                        <span style={{ fontSize: '13px', fontWeight: '600', color: '#334155' }}>{cat.category}</span>
                                        <span style={{ fontSize: '12px', fontWeight: 'bold', color: cat.completion_percentage === 100 ? '#16a34a' : '#475569' }}>
                                            {cat.completion_percentage}%
                                        </span>
                                    </div>
                                    <div style={{ width: '100%', backgroundColor: '#e2e8f0', borderRadius: '3px', height: '5px', overflow: 'hidden' }}>
                                        <div style={{ width: `${cat.completion_percentage}%`, backgroundColor: cat.completion_percentage === 100 ? '#16a34a' : '#0066cc', height: '100%' }}></div>
                                    </div>
                                    <div style={{ fontSize: '11px', color: '#94a3b8', marginTop: '4px', textAlign: 'right' }}>
                                        {cat.completed_tasks} / {cat.total_tasks} tasks
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Derived Section 3: Weakness Summary & Mistakes to Review */}
                    <div style={{ padding: '20px', backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px', marginBottom: '15px' }}>
                            <div>
                                <h4 style={{ margin: 0, fontSize: '15px', color: '#1e293b' }}>
                                    Active Weaknesses & Top Mistakes to Review
                                </h4>
                                <span style={{ fontSize: '13px', color: '#64748b' }}>
                                    Current unresolved conceptual errors logged in Weakness Manager.
                                </span>
                            </div>
                            <div style={{ display: 'flex', gap: '8px' }}>
                                <span style={{ fontSize: '12px', padding: '3px 8px', borderRadius: '4px', backgroundColor: '#fef3c7', color: '#92400e', fontWeight: 'bold' }}>
                                    Open: {reviewData.weakness_summary.open}
                                </span>
                                <span style={{ fontSize: '12px', padding: '3px 8px', borderRadius: '4px', backgroundColor: '#fee2e2', color: '#991b1b', fontWeight: 'bold' }}>
                                    High Priority: {reviewData.weakness_summary.high_priority}
                                </span>
                                <span style={{ fontSize: '12px', padding: '3px 8px', borderRadius: '4px', backgroundColor: '#dcfce7', color: '#166534', fontWeight: 'bold' }}>
                                    Resolved: {reviewData.weakness_summary.resolved}
                                </span>
                            </div>
                        </div>

                        {reviewData.mistakes_to_review.length === 0 ? (
                            <div style={{ padding: '20px', textAlign: 'center', backgroundColor: '#f8fafc', borderRadius: '6px', color: '#64748b', fontSize: '13px' }}>
                                No open mistakes logged. Great job keeping your mistake log clean!
                            </div>
                        ) : (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                                {reviewData.mistakes_to_review.map(item => (
                                    <div key={item.id} style={{ padding: '12px 14px', backgroundColor: '#f8fafc', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                                            <strong style={{ fontSize: '13px', color: '#0f172a' }}>{item.topic} — {item.problem_concept}</strong>
                                            <span style={{ fontSize: '11px', fontWeight: 'bold', padding: '2px 6px', borderRadius: '4px', backgroundColor: item.priority === 'CRITICAL' || item.priority === 'HIGH' ? '#fee2e2' : '#e0f2fe', color: item.priority === 'CRITICAL' || item.priority === 'HIGH' ? '#991b1b' : '#0369a1' }}>
                                                {item.priority}
                                            </span>
                                        </div>
                                        <div style={{ fontSize: '12px', color: '#dc2626', marginBottom: '3px' }}>
                                            <strong>Mistake:</strong> {item.what_i_got_wrong}
                                        </div>
                                        <div style={{ fontSize: '12px', color: '#16a34a' }}>
                                            <strong>Takeaway:</strong> {item.correct_concept}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Derived Section 4: Assessment & Mock Status */}
                    <div style={{ padding: '20px', backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px', marginBottom: '10px' }}>
                            <div>
                                <h4 style={{ margin: 0, fontSize: '15px', color: '#1e293b' }}>
                                    Weekly Assessment & Milestone Status
                                </h4>
                                <p style={{ margin: '3px 0 0 0', fontSize: '13px', color: '#64748b' }}>
                                    {reviewData.assessment_status}
                                </p>
                            </div>
                            <button
                                onClick={() => navigate('/app/assessments')}
                                style={{ padding: '6px 14px', backgroundColor: '#f1f5f9', color: '#0066cc', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '13px', fontWeight: 'bold', cursor: 'pointer' }}
                            >
                                {reviewData.assessment_info && reviewData.assessment_info.assessments_completed > 0 ? 'View All Assessments →' : 'Take Assessment →'}
                            </button>
                        </div>

                        {reviewData.assessment_info && reviewData.assessment_info.assessments_completed > 0 && (
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '10px', marginTop: '12px' }}>
                                <div style={{ padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px', border: '1px solid #f1f5f9' }}>
                                    <div style={{ fontSize: '11px', color: '#64748b', fontWeight: 'bold' }}>Attempts</div>
                                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#0f172a' }}>{reviewData.assessment_info.assessments_completed}</div>
                                </div>
                                <div style={{ padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px', border: '1px solid #f1f5f9' }}>
                                    <div style={{ fontSize: '11px', color: '#64748b', fontWeight: 'bold' }}>Latest Score</div>
                                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#0066cc' }}>{reviewData.assessment_info.latest_assessment_percentage}%</div>
                                </div>
                                <div style={{ padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px', border: '1px solid #f1f5f9' }}>
                                    <div style={{ fontSize: '11px', color: '#64748b', fontWeight: 'bold' }}>Average Score</div>
                                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#0f172a' }}>{reviewData.assessment_info.average_assessment_percentage}%</div>
                                </div>
                                <div style={{ padding: '8px 12px', backgroundColor: '#f0fdf4', borderRadius: '6px', border: '1px solid #bbf7d0' }}>
                                    <div style={{ fontSize: '11px', color: '#15803d', fontWeight: 'bold' }}>Passed</div>
                                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#166534' }}>{reviewData.assessment_info.passed_assessments}</div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* User Reflection Form */}
                    <div style={{ padding: '25px', backgroundColor: '#ffffff', borderRadius: '8px', border: '2px solid #0066cc', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', flexWrap: 'wrap', gap: '10px' }}>
                            <div>
                                <h3 style={{ margin: 0, color: '#1e293b' }}>
                                    Week {reviewData.week.week_number} Retrospective Reflection
                                </h3>
                                <p style={{ margin: '4px 0 0 0', color: '#64748b', fontSize: '13px' }}>
                                    Record qualitative self-evaluation, confidence scores, and priorities for the next week.
                                </p>
                            </div>
                            {reviewData.reflection?.updated_at && (
                                <span style={{ fontSize: '12px', color: '#64748b' }}>
                                    Last updated: {new Date(reviewData.reflection.updated_at).toLocaleString()}
                                </span>
                            )}
                        </div>

                        {saveSuccess && (
                            <div style={{ padding: '10px 14px', backgroundColor: '#dcfce7', border: '1px solid #86efac', borderRadius: '6px', color: '#166534', fontSize: '13px', marginBottom: '15px' }}>
                                ✓ Retrospective reflection saved successfully!
                            </div>
                        )}

                        <form onSubmit={handleSaveReflection} style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '18px' }}>
                                <TagListInput
                                    label="Weakest Topics this Week"
                                    placeholder="e.g. Subarray Sums, Tree DP (press Enter)"
                                    description="Topics where you struggled or got stuck."
                                    tags={reflectionForm.weakest_topics}
                                    onChange={(newTags) => setReflectionForm(prev => ({ ...prev, weakest_topics: newTags }))}
                                />

                                <TagListInput
                                    label="Improved Topics this Week"
                                    placeholder="e.g. Binary Search, Left Joins (press Enter)"
                                    description="Areas where you noticed genuine confidence gains."
                                    tags={reflectionForm.improved_topics}
                                    onChange={(newTags) => setReflectionForm(prev => ({ ...prev, improved_topics: newTags }))}
                                />

                                <TagListInput
                                    label="Carry-Forward Topics to Revisit"
                                    placeholder="e.g. Redo Dijkstra, OS Page Replacement (press Enter)"
                                    description="Unfinished concepts needing another study cycle."
                                    tags={reflectionForm.carry_forward_topics}
                                    onChange={(newTags) => setReflectionForm(prev => ({ ...prev, carry_forward_topics: newTags }))}
                                />

                                <TagListInput
                                    label="Next Week Key Priorities"
                                    placeholder="e.g. Complete 15 Trees problems, Mock interview (press Enter)"
                                    description="Concrete focus areas for the coming week."
                                    tags={reflectionForm.next_priorities}
                                    onChange={(newTags) => setReflectionForm(prev => ({ ...prev, next_priorities: newTags }))}
                                />
                            </div>

                            {/* Ratings: Confidence & Motivation */}
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '18px', padding: '15px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
                                <div>
                                    <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', color: '#334155', marginBottom: '6px' }}>
                                        Confidence Rating (1 - 5)
                                    </label>
                                    <select
                                        value={reflectionForm.confidence || ''}
                                        onChange={(e) => setReflectionForm(prev => ({ ...prev, confidence: e.target.value ? parseInt(e.target.value, 10) : null }))}
                                        style={{ width: '100%', padding: '8px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', backgroundColor: 'white' }}
                                    >
                                        <option value="">Select confidence...</option>
                                        {[1, 2, 3, 4, 5].map(n => (
                                            <option key={n} value={n}>{RATING_LABELS[n]}</option>
                                        ))}
                                    </select>
                                </div>

                                <div>
                                    <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', color: '#334155', marginBottom: '6px' }}>
                                        Motivation Rating (1 - 5)
                                    </label>
                                    <select
                                        value={reflectionForm.motivation || ''}
                                        onChange={(e) => setReflectionForm(prev => ({ ...prev, motivation: e.target.value ? parseInt(e.target.value, 10) : null }))}
                                        style={{ width: '100%', padding: '8px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', backgroundColor: 'white' }}
                                    >
                                        <option value="">Select motivation...</option>
                                        {[1, 2, 3, 4, 5].map(n => (
                                            <option key={n} value={n}>{RATING_LABELS[n]}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            {/* Schedule Adjustments */}
                            <div>
                                <label style={{ display: 'block', fontSize: '13px', fontWeight: 'bold', color: '#334155', marginBottom: '6px' }}>
                                    Schedule Adjustments & Free-Form Notes
                                </label>
                                <textarea
                                    rows="4"
                                    placeholder="Reflect on study pace, time management adjustments, or daily routine optimizations..."
                                    value={reflectionForm.schedule_adjustments}
                                    onChange={(e) => setReflectionForm(prev => ({ ...prev, schedule_adjustments: e.target.value }))}
                                    style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' }}
                                />
                            </div>

                            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
                                <button
                                    type="submit"
                                    disabled={saving}
                                    style={{
                                        padding: '10px 24px',
                                        backgroundColor: '#0066cc',
                                        color: 'white',
                                        border: 'none',
                                        borderRadius: '6px',
                                        fontWeight: 'bold',
                                        cursor: 'pointer',
                                        fontSize: '14px'
                                    }}
                                >
                                    {saving ? 'Saving Retrospective...' : 'Save Retrospective'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            ) : null}
        </div>
    );
};

export default WeeklyReview;
