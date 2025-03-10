import React, { useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

const Register = () => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '',
        hospital_name: '',
        hospital_type: 'private',
        registration_number: '',
    });

    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const { registerUser } = useContext(AuthContext);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

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
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                'Registration failed. Please check your information and try again.'
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
                                <i className="fas fa-hospital text-primary" style={{ fontSize: '3rem' }}></i>
                                <h2 className="mt-3">Create an Account</h2>
                                <p className="text-muted">Register your hospital</p>
                            </div>

                            {error && (
                                <div className="alert alert-danger" role="alert">
                                    {error}
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
                                <h5>Hospital Information</h5>

                                <div className="mb-3">
                                    <label htmlFor="hospital_name" className="form-label">Hospital Name</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="hospital_name"
                                        name="hospital_name"
                                        value={formData.hospital_name}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>

                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="hospital_type" className="form-label">Hospital Type</label>
                                        <select
                                            className="form-select"
                                            id="hospital_type"
                                            name="hospital_type"
                                            value={formData.hospital_type}
                                            onChange={handleChange}
                                            required
                                        >
                                            <option value="government">Government</option>
                                            <option value="private">Private</option>
                                            <option value="non_profit">Non-Profit</option>
                                            <option value="research">Research</option>
                                            <option value="teaching">Teaching</option>
                                        </select>
                                    </div>

                                    <div className="col-md-6 mb-3">
                                        <label htmlFor="registration_number" className="form-label">Registration Number</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            id="registration_number"
                                            name="registration_number"
                                            value={formData.registration_number}
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
                                        'Register'
                                    )}
                                </button>
                            </form>

                            <div className="text-center mt-4">
                                <p>
                                    Already have an account? <Link to="/login" className="text-primary">Sign In</Link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register; 