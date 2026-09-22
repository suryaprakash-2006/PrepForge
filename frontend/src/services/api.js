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

export const getWeaknesses = async (token, params = {}) => {
    const url = new URL(`${API_BASE_URL}/api/v1/weaknesses`);
    if (params.status) url.searchParams.append('status', params.status);
    if (params.priority) url.searchParams.append('priority', params.priority);
    if (params.topic) url.searchParams.append('topic', params.topic);
    
    const response = await fetch(url, {
        method: 'GET',
        headers: getHeaders(token)
    });
    if (!response.ok) throw new Error('Failed to fetch weaknesses');
    return await response.json();
};

export const getWeakness = async (token, id) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/weaknesses/${id}`, {
        method: 'GET',
        headers: getHeaders(token)
    });
    if (!response.ok) throw new Error('Failed to fetch weakness');
    return await response.json();
};

export const createWeakness = async (token, data) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/weaknesses`, {
        method: 'POST',
        headers: getHeaders(token),
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Failed to create weakness');
    }
    return await response.json();
};

export const updateWeakness = async (token, id, data) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/weaknesses/${id}`, {
        method: 'PATCH',
        headers: getHeaders(token),
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Failed to update weakness');
    }
    return await response.json();
};

export const deleteWeakness = async (token, id) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/weaknesses/${id}`, {
        method: 'DELETE',
        headers: getHeaders(token)
    });
    if (!response.ok) throw new Error('Failed to delete weakness');
    return true;
};

export const getWeeklyReview = async (token, weekNumber) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/weekly-reviews/${weekNumber}`, {
        method: 'GET',
        headers: getHeaders(token)
    });
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Failed to fetch weekly review');
    }
    return await response.json();
};

export const saveWeeklyReview = async (token, weekNumber, data) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/weekly-reviews/${weekNumber}`, {
        method: 'PUT',
        headers: getHeaders(token),
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Failed to save weekly review');
    }
    return await response.json();
};

