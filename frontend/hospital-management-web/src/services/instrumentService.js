import api from './api';

export const getInstruments = (params) => {
    return api.get('/instruments/instruments/', { params });
};

export const getInstrument = (id) => {
    return api.get(`/instruments/instruments/${id}/`);
};

export const createInstrument = (instrumentData) => {
    return api.post('/instruments/instruments/', instrumentData);
};

export const updateInstrument = (id, instrumentData) => {
    return api.put(`/instruments/instruments/${id}/`, instrumentData);
};

export const deleteInstrument = (id) => {
    return api.delete(`/instruments/instruments/${id}/`);
};

export const getInstrumentCategories = () => {
    return api.get('/instruments/categories/');
};

export const createInstrumentCategory = (categoryData) => {
    return api.post('/instruments/categories/', categoryData);
};

export const getInstrumentMaintenance = (instrumentId) => {
    return api.get(`/instruments/maintenance/?instrument=${instrumentId}`);
};

export const createInstrumentMaintenance = (maintenanceData) => {
    return api.post('/instruments/maintenance/', maintenanceData);
}; 