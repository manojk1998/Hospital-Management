import React, { createContext, useState, useEffect } from 'react';
import { login, register, logout, checkAuth } from '../services/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Check if user is authenticated on page load
        const checkAuthentication = async () => {
            try {
                const token = localStorage.getItem('token');
                if (token) {
                    const response = await checkAuth();
                    setUser(response.data);
                    setIsAuthenticated(true);
                }
            } catch (error) {
                console.error('Authentication check failed:', error);
                localStorage.removeItem('token');
                setUser(null);
                setIsAuthenticated(false);
            } finally {
                setLoading(false);
            }
        };

        checkAuthentication();
    }, []);

    const loginUser = async (email, password) => {
        setLoading(true);
        setError(null);
        try {
            const response = await login(email, password);
            localStorage.setItem('token', response.data.access);
            localStorage.setItem('refreshToken', response.data.refresh);
            setUser(response.data.user);
            setIsAuthenticated(true);
            return response.data;
        } catch (error) {
            setError(error.response?.data?.detail || 'Login failed. Please check your credentials.');
            throw error;
        } finally {
            setLoading(false);
        }
    };

    const registerUser = async (userData) => {
        setLoading(true);
        setError(null);
        try {
            const response = await register(userData);
            localStorage.setItem('token', response.data.access);
            localStorage.setItem('refreshToken', response.data.refresh);
            setUser(response.data.user);
            setIsAuthenticated(true);
            return response.data;
        } catch (error) {
            setError(error.response?.data?.detail || 'Registration failed. Please try again.');
            throw error;
        } finally {
            setLoading(false);
        }
    };

    const logoutUser = async () => {
        setLoading(true);
        try {
            await logout();
            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
            setUser(null);
            setIsAuthenticated(false);
        } catch (error) {
            console.error('Logout failed:', error);
        } finally {
            setLoading(false);
        }
    };

    const updateUser = (userData) => {
        setUser(userData);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated,
                loading,
                error,
                loginUser,
                registerUser,
                logoutUser,
                updateUser,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}; 