import React, { createContext, useState, useEffect, useContext } from 'react';
import { login as apiLogin, register as apiRegister, getCurrentUser } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [authenticated, setAuthenticated] = useState(false);

    useEffect(() => {
        const initAuth = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const userData = await getCurrentUser(token);
                    setUser(userData);
                    setAuthenticated(true);
                } catch (error) {
                    // Token invalid or expired
                    localStorage.removeItem('token');
                    setUser(null);
                    setAuthenticated(false);
                }
            }
            setLoading(false);
        };
        initAuth();
    }, []);

    const login = async (email, password) => {
        const data = await apiLogin(email, password);
        const token = data.access_token;
        localStorage.setItem('token', token);
        
        const userData = await getCurrentUser(token);
        setUser(userData);
        setAuthenticated(true);
    };

    const register = async (name, email, password) => {
        return await apiRegister(name, email, password);
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
        setAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ user, loading, authenticated, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
