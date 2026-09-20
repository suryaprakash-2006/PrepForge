import React, { useState } from 'react';
import { useNavigate, Link, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Register = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    
    const { register, authenticated, loading } = useAuth();
    const navigate = useNavigate();

    if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;
    if (authenticated) return <Navigate to="/app" replace />;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        
        if (password.length < 8) {
            return setError('Password must be at least 8 characters.');
        }
        if (password !== confirmPassword) {
            return setError('Passwords do not match.');
        }

        setIsSubmitting(true);
        try {
            await register(name, email, password);
            navigate('/login');
        } catch (err) {
            setError(err.message || 'Registration failed');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '40px auto', padding: '30px', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
            <h1 style={{ marginTop: 0, textAlign: 'center' }}>PrepForge</h1>
            <h2 style={{ textAlign: 'center', color: '#555', marginBottom: '20px' }}>Create Account</h2>
            
            {error && <div style={{ backgroundColor: '#fee', color: 'red', padding: '10px', borderRadius: '4px', marginBottom: '20px', border: '1px solid #fcc' }}>{error}</div>}
            
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <div>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Name</label>
                    <input 
                        type="text" 
                        value={name} 
                        onChange={e => setName(e.target.value)}
                        required
                        style={{ width: '100%', padding: '10px', boxSizing: 'border-box', border: '1px solid #ccc', borderRadius: '4px' }}
                    />
                </div>
                
                <div>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Email</label>
                    <input 
                        type="email" 
                        value={email} 
                        onChange={e => setEmail(e.target.value)}
                        required
                        style={{ width: '100%', padding: '10px', boxSizing: 'border-box', border: '1px solid #ccc', borderRadius: '4px' }}
                    />
                </div>
                
                <div>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Password</label>
                    <input 
                        type="password" 
                        value={password} 
                        onChange={e => setPassword(e.target.value)}
                        required
                        style={{ width: '100%', padding: '10px', boxSizing: 'border-box', border: '1px solid #ccc', borderRadius: '4px' }}
                    />
                </div>

                <div>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Confirm Password</label>
                    <input 
                        type="password" 
                        value={confirmPassword} 
                        onChange={e => setConfirmPassword(e.target.value)}
                        required
                        style={{ width: '100%', padding: '10px', boxSizing: 'border-box', border: '1px solid #ccc', borderRadius: '4px' }}
                    />
                </div>
                
                <button 
                    type="submit" 
                    disabled={isSubmitting}
                    style={{ padding: '12px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: isSubmitting ? 'not-allowed' : 'pointer', fontSize: '16px', marginTop: '10px' }}
                >
                    {isSubmitting ? 'Creating...' : 'Create Account'}
                </button>
            </form>
            
            <div style={{ marginTop: '20px', textAlign: 'center', fontSize: '14px' }}>
                Already have an account? <Link to="/login" style={{ color: '#0066cc', textDecoration: 'none' }}>Login</Link>
            </div>
        </div>
    );
};

export default Register;
