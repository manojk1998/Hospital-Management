import api from './api';

export const getClients = (params) => {
    return api.get('/clients/clients/', { params });
};

export const getClient = (id) => {
    return api.get(`/clients/clients/${id}/`);
};

export const createClient = (clientData) => {
    return api.post('/clients/clients/', clientData);
};

export const updateClient = (id, clientData) => {
    return api.put(`/clients/clients/${id}/`, clientData);
};

export const deleteClient = (id) => {
    return api.delete(`/clients/clients/${id}/`);
};

export const getClientContacts = (clientId) => {
    return api.get(`/clients/contacts/?client=${clientId}`);
};

export const createClientContact = (contactData) => {
    return api.post('/clients/contacts/', contactData);
};

export const updateClientContact = (id, contactData) => {
    return api.put(`/clients/contacts/${id}/`, contactData);
};

export const deleteClientContact = (id) => {
    return api.delete(`/clients/contacts/${id}/`);
};

export const getClientAddresses = (clientId) => {
    return api.get(`/clients/addresses/?client=${clientId}`);
};

export const createClientAddress = (addressData) => {
    return api.post('/clients/addresses/', addressData);
};

export const updateClientAddress = (id, addressData) => {
    return api.put(`/clients/addresses/${id}/`, addressData);
};

export const deleteClientAddress = (id) => {
    return api.delete(`/clients/addresses/${id}/`);
}; 