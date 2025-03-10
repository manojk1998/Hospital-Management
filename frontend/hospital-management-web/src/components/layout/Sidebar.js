import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = ({ isOpen, userRole }) => {
    const isAdmin = userRole === 'admin';
    const isStaff = userRole === 'staff';
    const isClient = userRole === 'client';

    return (
        <div className={`sidebar ${!isOpen ? 'closed' : ''}`}>
            <ul className="sidebar-menu">
                <li className="sidebar-menu-item">
                    <Link to="/">
                        <i className="fas fa-tachometer-alt"></i>
                        Dashboard
                    </Link>
                </li>

                {(isAdmin || isStaff) && (
                    <li className="sidebar-menu-item">
                        <Link to="/instruments">
                            <i className="fas fa-microscope"></i>
                            Instruments
                        </Link>
                    </li>
                )}

                {(isAdmin || isStaff) && (
                    <li className="sidebar-menu-item">
                        <Link to="/clients">
                            <i className="fas fa-hospital-user"></i>
                            Clients
                        </Link>
                    </li>
                )}

                {isAdmin && (
                    <li className="sidebar-menu-item">
                        <Link to="/staff">
                            <i className="fas fa-user-md"></i>
                            Staff
                        </Link>
                    </li>
                )}

                <li className="sidebar-menu-item">
                    <Link to="/orders">
                        <i className="fas fa-shopping-cart"></i>
                        Orders
                    </Link>
                </li>

                {(isAdmin || isStaff) && (
                    <li className="sidebar-menu-item">
                        <Link to="/reports">
                            <i className="fas fa-chart-bar"></i>
                            Reports
                        </Link>
                    </li>
                )}

                <li className="sidebar-menu-item">
                    <Link to="/notifications">
                        <i className="fas fa-bell"></i>
                        Notifications
                    </Link>
                </li>

                <li className="sidebar-menu-item">
                    <Link to="/profile">
                        <i className="fas fa-user-circle"></i>
                        Profile
                    </Link>
                </li>

                {isAdmin && (
                    <li className="sidebar-menu-item">
                        <Link to="/register">
                            <i className="fas fa-user-plus"></i>
                            Register Staff
                        </Link>
                    </li>
                )}
            </ul>
        </div>
    );
};

export default Sidebar; 