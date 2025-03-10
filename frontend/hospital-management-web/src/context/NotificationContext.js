import React, { createContext, useState, useEffect, useContext } from 'react';
import { getNotifications, markAsRead } from '../services/notificationService';
import { AuthContext } from './AuthContext';

export const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
    const [notifications, setNotifications] = useState([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [loading, setLoading] = useState(false);
    const { isAuthenticated } = useContext(AuthContext);

    useEffect(() => {
        if (isAuthenticated) {
            fetchNotifications();
        }
    }, [isAuthenticated]);

    const fetchNotifications = async () => {
        setLoading(true);
        try {
            const response = await getNotifications();
            setNotifications(response.data);
            setUnreadCount(response.data.filter(notification => !notification.is_read).length);
        } catch (error) {
            console.error('Failed to fetch notifications:', error);
        } finally {
            setLoading(false);
        }
    };

    const markNotificationAsRead = async (id) => {
        try {
            await markAsRead(id);
            setNotifications(prevNotifications =>
                prevNotifications.map(notification =>
                    notification.id === id ? { ...notification, is_read: true } : notification
                )
            );
            setUnreadCount(prevCount => Math.max(0, prevCount - 1));
        } catch (error) {
            console.error('Failed to mark notification as read:', error);
        }
    };

    const markAllAsRead = async () => {
        try {
            await Promise.all(
                notifications
                    .filter(notification => !notification.is_read)
                    .map(notification => markAsRead(notification.id))
            );
            setNotifications(prevNotifications =>
                prevNotifications.map(notification => ({ ...notification, is_read: true }))
            );
            setUnreadCount(0);
        } catch (error) {
            console.error('Failed to mark all notifications as read:', error);
        }
    };

    const addNotification = (notification) => {
        setNotifications(prevNotifications => [notification, ...prevNotifications]);
        if (!notification.is_read) {
            setUnreadCount(prevCount => prevCount + 1);
        }
    };

    return (
        <NotificationContext.Provider
            value={{
                notifications,
                unreadCount,
                loading,
                fetchNotifications,
                markNotificationAsRead,
                markAllAsRead,
                addNotification,
            }}
        >
            {children}
        </NotificationContext.Provider>
    );
}; 