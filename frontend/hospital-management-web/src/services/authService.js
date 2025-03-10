import api from './api';

export const login = (email, password) => {
    return api.post('/accounts/token/', { email, password });
};

export const register = (userData) => {
    return api.post('/accounts/register/', userData);
};

export const logout = () => {
    return api.post('/accounts/logout/');
};

export const checkAuth = () => {
    return api.get('/accounts/me/');
};

export const updateProfile = (userData) => {
    return api.put('/accounts/me/', userData);
};

export const changePassword = (passwordData) => {
    return api.post('/accounts/change-password/', passwordData);
}; 