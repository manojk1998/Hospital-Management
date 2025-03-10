import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Components
import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';
import Footer from './components/layout/Footer';
import PrivateRoute from './components/common/PrivateRoute';
import Loader from './components/common/Loader';

// Pages
import Dashboard from './pages/Dashboard';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import InstrumentsList from './pages/instruments/InstrumentsList';
import InstrumentDetails from './pages/instruments/InstrumentDetails';
import ClientsList from './pages/clients/ClientsList';
import ClientDetails from './pages/clients/ClientDetails';
import StaffList from './pages/staff/StaffList';
import StaffDetails from './pages/staff/StaffDetails';
import OrdersList from './pages/orders/OrdersList';
import OrderDetails from './pages/orders/OrderDetails';
import CreateOrder from './pages/orders/CreateOrder';
import ReportsList from './pages/reports/ReportsList';
import NotificationsList from './pages/notifications/NotificationsList';
import Profile from './pages/profile/Profile';

// Services
import { checkAuth } from './services/authService';

// CSS
import './App.css';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [sidebarOpen, setSidebarOpen] = useState(true);

    useEffect(() => {
        // Check if user is authenticated
        const checkAuthentication = async () => {
            try {
                const response = await checkAuth();
                setIsAuthenticated(true);
                setUser(response.data);
            } catch (error) {
                setIsAuthenticated(false);
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        checkAuthentication();
    }, []);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    if (loading) {
        return <Loader />;
    }

    return (
        <Router>
            <div className="app-container">
                {isAuthenticated && <Navbar user={user} toggleSidebar={toggleSidebar} />}

                <div className="content-container">
                    {isAuthenticated && <Sidebar isOpen={sidebarOpen} userRole={user?.role} />}

                    <main className={`main-content ${isAuthenticated && sidebarOpen ? 'with-sidebar' : ''}`}>
                        <Routes>
                            {/* Public Routes */}
                            <Route path="/login" element={!isAuthenticated ? <Login setAuth={setIsAuthenticated} setUser={setUser} /> : <Navigate to="/" />} />
                            <Route path="/register" element={!isAuthenticated ? <Register setAuth={setIsAuthenticated} setUser={setUser} /> : <Navigate to="/" />} />

                            {/* Private Routes */}
                            <Route path="/" element={<PrivateRoute isAuthenticated={isAuthenticated}><Dashboard /></PrivateRoute>} />

                            {/* Instruments Routes */}
                            <Route path="/instruments" element={<PrivateRoute isAuthenticated={isAuthenticated}><InstrumentsList /></PrivateRoute>} />
                            <Route path="/instruments/:id" element={<PrivateRoute isAuthenticated={isAuthenticated}><InstrumentDetails /></PrivateRoute>} />

                            {/* Clients Routes */}
                            <Route path="/clients" element={<PrivateRoute isAuthenticated={isAuthenticated}><ClientsList /></PrivateRoute>} />
                            <Route path="/clients/:id" element={<PrivateRoute isAuthenticated={isAuthenticated}><ClientDetails /></PrivateRoute>} />

                            {/* Staff Routes */}
                            <Route path="/staff" element={<PrivateRoute isAuthenticated={isAuthenticated}><StaffList /></PrivateRoute>} />
                            <Route path="/staff/:id" element={<PrivateRoute isAuthenticated={isAuthenticated}><StaffDetails /></PrivateRoute>} />

                            {/* Orders Routes */}
                            <Route path="/orders" element={<PrivateRoute isAuthenticated={isAuthenticated}><OrdersList /></PrivateRoute>} />
                            <Route path="/orders/create" element={<PrivateRoute isAuthenticated={isAuthenticated}><CreateOrder /></PrivateRoute>} />
                            <Route path="/orders/:id" element={<PrivateRoute isAuthenticated={isAuthenticated}><OrderDetails /></PrivateRoute>} />

                            {/* Reports Routes */}
                            <Route path="/reports" element={<PrivateRoute isAuthenticated={isAuthenticated}><ReportsList /></PrivateRoute>} />

                            {/* Notifications Routes */}
                            <Route path="/notifications" element={<PrivateRoute isAuthenticated={isAuthenticated}><NotificationsList /></PrivateRoute>} />

                            {/* Profile Routes */}
                            <Route path="/profile" element={<PrivateRoute isAuthenticated={isAuthenticated}><Profile user={user} setUser={setUser} /></PrivateRoute>} />

                            {/* Fallback Route */}
                            <Route path="*" element={<Navigate to="/" />} />
                        </Routes>
                    </main>
                </div>

                {isAuthenticated && <Footer />}
            </div>
        </Router>
    );
}

export default App; 