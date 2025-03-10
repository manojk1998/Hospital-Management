import api from './api';

export const getStaffMembers = (params) => {
    return api.get('/staff/members/', { params });
};

export const getStaffMember = (id) => {
    return api.get(`/staff/members/${id}/`);
};

export const createStaffMember = (staffData) => {
    return api.post('/staff/members/', staffData);
};

export const updateStaffMember = (id, staffData) => {
    return api.put(`/staff/members/${id}/`, staffData);
};

export const deleteStaffMember = (id) => {
    return api.delete(`/staff/members/${id}/`);
};

export const getStaffDepartments = () => {
    return api.get('/staff/departments/');
};

export const createStaffDepartment = (departmentData) => {
    return api.post('/staff/departments/', departmentData);
};

export const updateStaffDepartment = (id, departmentData) => {
    return api.put(`/staff/departments/${id}/`, departmentData);
};

export const deleteStaffDepartment = (id) => {
    return api.delete(`/staff/departments/${id}/`);
};

export const getAttendance = (params) => {
    return api.get('/staff/attendance/', { params });
};

export const checkIn = () => {
    return api.post('/staff/attendance/check_in/');
};

export const checkOut = () => {
    return api.post('/staff/attendance/check_out/');
};

export const getLeaves = (params) => {
    return api.get('/staff/leaves/', { params });
};

export const applyLeave = (leaveData) => {
    return api.post('/staff/leaves/', leaveData);
};

export const approveLeave = (id) => {
    return api.post(`/staff/leaves/${id}/approve/`);
};

export const rejectLeave = (id, rejectionReason) => {
    return api.post(`/staff/leaves/${id}/reject/`, { rejection_reason: rejectionReason });
}; 