import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import { NotificationContext } from '../../context/NotificationContext';

const Navbar = ({ toggleSidebar }) => {
    const { user, logoutUser } = useContext(AuthContext);
    const { unreadCount } = useContext(NotificationContext);

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <button
                    className="btn btn-outline-secondary me-2"
                    onClick={toggleSidebar}
                >
                    <i className="fas fa-bars"></i>
                </button>

                <Link className="navbar-brand" to="/">
                    <i className="fas fa-hospital me-2"></i>
                    Hospital Instrument Management
                </Link>

                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto">
                        <li className="nav-item">
                            <Link className="nav-link position-relative" to="/notifications">
                                <i className="fas fa-bell"></i>
                                {unreadCount > 0 && (
                                    <span className="notification-badge">{unreadCount}</span>
                                )}
                            </Link>
                        </li>

                        <li className="nav-item dropdown">
                            <a
                                className="nav-link dropdown-toggle"
                                href="#"
                                id="navbarDropdown"
                                role="button"
                                data-bs-toggle="dropdown"
                            >
                                <i className="fas fa-user me-1"></i>
                                {user?.first_name || 'User'}
                            </a>
                            <ul className="dropdown-menu dropdown-menu-end">
                                <li>
                                    <Link className="dropdown-item" to="/profile">
                                        <i className="fas fa-id-card me-2"></i>
                                        Profile
                                    </Link>
                                </li>
                                <li><hr className="dropdown-divider" /></li>
                                <li>
                                    <button
                                        className="dropdown-item text-danger"
                                        onClick={logoutUser}
                                    >
                                        <i className="fas fa-sign-out-alt me-2"></i>
                                        Logout
                                    </button>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar; 