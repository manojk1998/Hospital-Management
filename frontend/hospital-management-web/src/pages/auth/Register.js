import React, { useState, useContext } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

const Register = () => {
    const { user, isAuthenticated, registerUser } = useContext(AuthContext);

    // Initialize state at the top level, before any conditional returns
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '',
        employee_id: '',
        role: 'staff',
        department: '',
        date_of_joining: new Date().toISOString().split('T')[0]
    });

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    // Redirect if not authenticated or not an admin
    if (!isAuthenticated || (user && user.role !== 'admin')) {
        return <Navigate to="/" />;
    }

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        // Validate passwords match
        if (formData.password !== formData.confirm_password) {
            setError('Passwords do not match');
            return;
        }

        setIsLoading(true);

        try {
            // Remove confirm_password before sending to API
            const { confirm_password, ...registerData } = formData;
            await registerUser(registerData);
            setSuccess('Staff member registered successfully!');

            // Reset form
            setFormData({
                first_name: '',
                last_name: '',
                email: '',
                password: '',
                confirm_password: '',
                employee_id: '',
                role: 'staff',
                department: '',
                date_of_joining: new Date().toISOString().split('T')[0]
            });
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                'Registration failed. Please check the information and try again.'
            );
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="row justify-content-center my-5">
                <div className="col-md-8 col-lg-6">
                    <div className="card shadow">
                        <div className="card-body p-5">
                            <div className="text-center mb-4">
                                <i className="fas fa-user-plus text-primary" style={{ fontSize: '3rem' }}></i>
                                <h2 className="mt-3">Register New Staff Member</h2>
                                <p className="text-muted">Add a new staff member to the system</p>
                            </div>

                            {error && (
                                <div className="alert alert-danger" role="alert">
                                    {error}
                                </div>
                            )}

                            {success && (
                                <div className="alert alert-success" role="alert">
                                    {success}
                                </div>
                            )}

                            <form onSubmit={handleSubmit}>
                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="first_name" className="form-label">First Name</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            id="first_name"
                                            name="first_name"
                                            value={formData.first_name}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>

                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="last_name" className="form-label">Last Name</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            id="last_name"
                                            name="last_name"
                                            value={formData.last_name}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="email" className="form-label">Email address</label>
                                    <input
                                        type="email"
                                        className="form-control"
                                        id="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>

                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="password" className="form-label">Password</label>
                                        <input
                                            type="password"
                                            className="form-control"
                                            id="password"
                                            name="password"
                                            value={formData.password}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>

                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="confirm_password" className="form-label">Confirm Password</label>
                                        <input
                                            type="password"
                                            className="form-control"
                                            id="confirm_password"
                                            name="confirm_password"
                                            value={formData.confirm_password}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>
                                </div>

                                <hr className="my-4" />
                                <h5>Staff Information</h5>

                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="employee_id" className="form-label">Employee ID</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            id="employee_id"
                                            name="employee_id"
                                            value={formData.employee_id}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>

                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="role" className="form-label">Role</label>
                                        <select
                                            className="form-select"
                                            id="role"
                                            name="role"
                                            value={formData.role}
                                            onChange={handleChange}
                                            required
                                        >
                                            <option value="staff">Staff</option>
                                            <option value="admin">Administrator</option>
                                        </select>
                                    </div>
                                </div>

                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="department" className="form-label">Department</label>
                                        <select
                                            className="form-select"
                                            id="department"
                                            name="department"
                                            value={formData.department}
                                            onChange={handleChange}
                                            required
                                        >
                                            <option value="">Select Department</option>
                                            <option value="1">Sales</option>
                                            <option value="2">Support</option>
                                            <option value="3">Technical</option>
                                            <option value="4">Management</option>
                                        </select>
                                    </div>

                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="date_of_joining" className="form-label">Date of Joining</label>
                                        <input
                                            type="date"
                                            className="form-control"
                                            id="date_of_joining"
                                            name="date_of_joining"
                                            value={formData.date_of_joining}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>
                                </div>

                                <button
                                    type="submit"
                                    className="btn btn-primary w-100 py-2 mt-3"
                                    disabled={isLoading}
                                >
                                    {isLoading ? (
                                        <>
                                            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                            Registering...
                                        </>
                                    ) : (
                                        'Register Staff Member'
                                    )}
                                </button>
                            </form>

                            <div className="text-center mt-4">
                                <Link to="/" className="btn btn-outline-secondary">
                                    <i className="fas fa-arrow-left me-2"></i>
                                    Back to Dashboard
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register; 