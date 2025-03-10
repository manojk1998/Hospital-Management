import api from './api';

export const getOrders = (params) => {
    return api.get('/orders/orders/', { params });
};

export const getOrder = (id) => {
    return api.get(`/orders/orders/${id}/`);
};

export const createOrder = (orderData) => {
    return api.post('/orders/orders/', orderData);
};

export const updateOrder = (id, orderData) => {
    return api.put(`/orders/orders/${id}/`, orderData);
};

export const deleteOrder = (id) => {
    return api.delete(`/orders/orders/${id}/`);
};

export const cancelOrder = (id) => {
    return api.post(`/orders/orders/${id}/cancel/`);
};

export const generateInvoice = (id) => {
    return api.post(`/orders/orders/${id}/generate_invoice/`);
};

export const getOrderItems = (orderId) => {
    return api.get(`/orders/items/?order=${orderId}`);
};

export const getPayments = (params) => {
    return api.get('/orders/payments/', { params });
};

export const createPayment = (paymentData) => {
    return api.post('/orders/payments/', paymentData);
};

export const getInvoices = (params) => {
    return api.get('/orders/invoices/', { params });
};

export const getInvoice = (id) => {
    return api.get(`/orders/invoices/${id}/`);
};

export const sendInvoice = (id) => {
    return api.post(`/orders/invoices/${id}/send/`);
};

export const markInvoiceAsPaid = (id) => {
    return api.post(`/orders/invoices/${id}/mark_paid/`);
}; 