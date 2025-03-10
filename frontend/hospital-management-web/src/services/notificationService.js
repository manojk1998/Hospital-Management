import api from './api';

export const getNotifications = (params) => {
    return api.get('/notifications/notifications/', { params });
};

export const markAsRead = (id) => {
    return api.post(`/notifications/notifications/${id}/mark_as_read/`);
};

export const markAllAsRead = () => {
    return api.post('/notifications/notifications/mark_all_as_read/');
};

export const getEmailNotifications = (params) => {
    return api.get('/notifications/emails/', { params });
};

export const createEmailNotification = (emailData) => {
    return api.post('/notifications/emails/', emailData);
};

export const sendEmail = (id) => {
    return api.post(`/notifications/emails/${id}/send/`);
};

export const getSMSNotifications = (params) => {
    return api.get('/notifications/sms/', { params });
};

export const createSMSNotification = (smsData) => {
    return api.post('/notifications/sms/', smsData);
};

export const sendSMS = (id) => {
    return api.post(`/notifications/sms/${id}/send/`);
}; 