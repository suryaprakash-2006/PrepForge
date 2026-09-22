const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const getHeaders = (token = null) => {
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
};

export const getHealth = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/health`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Health check failed:", error);
        return { status: "error", message: error.message };
    }
};

export const register = async (name, email, password) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ name, email, password })
    });
    
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Registration failed');
    }
    
    return await response.json();
};

export const login = async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Login failed');
    }
    
    return await response.json();
};

export const getCurrentUser = async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
        method: 'GET',
        headers: getHeaders(token)
    });
    
    if (!response.ok) {
        throw new Error('Unauthorized');
    }
    
    return await response.json();
};

export const getWeeks = async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/weeks`, {
        method: 'GET',
        headers: getHeaders(token)
    });
    if (!response.ok) throw new Error('Failed to fetch weeks');
    return await response.json();
};

export const initializeRoadmap = async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/weeks/initialize`, {
        method: 'POST',
        headers: getHeaders(token)
    });
    if (!response.ok) throw new Error('Failed to initialize roadmap');
    return await response.json();
};

export const getTasks = async (token, weekId) => {
    const url = new URL(`${API_BASE_URL}/api/v1/tasks`);
    if (weekId) {
        url.searchParams.append('week_id', weekId);
    }
    const response = await fetch(url, {
        method: 'GET',
        headers: getHeaders(token)
    });
    if (!response.ok) throw new Error('Failed to fetch tasks');
    return await response.json();
};

export const updateTask = async (token, taskId, data) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/tasks/${taskId}`, {
        method: 'PATCH',
        headers: getHeaders(token),
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to update task');
    return await response.json();
};

export const getDashboard = async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/dashboard`, {
        method: 'GET',
        headers: getHeaders(token)
    });
    if (!response.ok) throw new Error('Failed to fetch dashboard data');
    return await response.json();
};
