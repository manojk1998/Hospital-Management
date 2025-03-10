import api from './api';

export const getReports = (params) => {
    return api.get('/reports/reports/', { params });
};

export const getReport = (id) => {
    return api.get(`/reports/reports/${id}/`);
};

export const generateReport = (reportData) => {
    return api.post('/reports/reports/generate/', reportData);
};

export const downloadReport = (id) => {
    return api.get(`/reports/reports/${id}/download/`, {
        responseType: 'blob'
    });
};

export const getDashboards = () => {
    return api.get('/reports/dashboards/');
};

export const getDefaultDashboard = () => {
    return api.get('/reports/dashboards/default/');
};

export const getDashboard = (id) => {
    return api.get(`/reports/dashboards/${id}/`);
};

export const createDashboard = (dashboardData) => {
    return api.post('/reports/dashboards/', dashboardData);
};

export const updateDashboard = (id, dashboardData) => {
    return api.put(`/reports/dashboards/${id}/`, dashboardData);
};

export const deleteDashboard = (id) => {
    return api.delete(`/reports/dashboards/${id}/`);
};

export const getWidgets = (dashboardId) => {
    return api.get(`/reports/widgets/?dashboard=${dashboardId}`);
};

export const getWidget = (id) => {
    return api.get(`/reports/widgets/${id}/`);
};

export const createWidget = (widgetData) => {
    return api.post('/reports/widgets/', widgetData);
};

export const updateWidget = (id, widgetData) => {
    return api.put(`/reports/widgets/${id}/`, widgetData);
};

export const deleteWidget = (id) => {
    return api.delete(`/reports/widgets/${id}/`);
};

export const getWidgetData = (id, params) => {
    return api.get(`/reports/widgets/${id}/data/`, { params });
}; 