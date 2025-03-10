import React, { useState, useEffect, useContext, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Chart } from 'chart.js/auto';
import { AuthContext } from '../context/AuthContext';
import Loader from '../components/common/Loader';
import { getDefaultDashboard, getWidgetData } from '../services/reportService';
import { getInstruments } from '../services/instrumentService';
import { getOrders } from '../services/orderService';
import { getClients } from '../services/clientService';

const Dashboard = () => {
    const { user } = useContext(AuthContext);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState({
        totalInstruments: 0,
        availableInstruments: 0,
        totalOrders: 0,
        totalClients: 0,
        revenue: 0
    });
    const [recentOrders, setRecentOrders] = useState([]);
    const [dashboard, setDashboard] = useState(null);

    const instrumentChartRef = useRef(null);
    const revenueChartRef = useRef(null);
    const instrumentChartInstance = useRef(null);
    const revenueChartInstance = useRef(null);

    useEffect(() => {
        const fetchDashboardData = async () => {
            setLoading(true);
            try {
                // Fetch dashboard configuration
                const dashboardResponse = await getDefaultDashboard();
                setDashboard(dashboardResponse.data);

                // Fetch instruments stats
                const instrumentsResponse = await getInstruments();
                const instruments = instrumentsResponse.data.results || [];
                const availableInstruments = instruments.filter(i => i.status === 'available').length;

                // Fetch orders
                const ordersResponse = await getOrders({ limit: 5, ordering: '-order_date' });
                const orders = ordersResponse.data.results || [];
                setRecentOrders(orders);

                // Fetch clients
                const clientsResponse = await getClients();
                const clients = clientsResponse.data.results || [];

                // Calculate total revenue
                const revenue = orders.reduce((total, order) => total + parseFloat(order.grand_total), 0);

                // Set stats
                setStats({
                    totalInstruments: instruments.length,
                    availableInstruments,
                    totalOrders: orders.length,
                    totalClients: clients.length,
                    revenue
                });

                // Create charts
                createInstrumentChart(instruments);
                createRevenueChart(orders);

            } catch (error) {
                console.error('Error fetching dashboard data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();

        // Cleanup charts on unmount
        return () => {
            if (instrumentChartInstance.current) {
                instrumentChartInstance.current.destroy();
            }
            if (revenueChartInstance.current) {
                revenueChartInstance.current.destroy();
            }
        };
    }, []);

    const createInstrumentChart = (instruments) => {
        if (instrumentChartRef.current) {
            // Count instruments by status
            const statusCounts = {
                available: 0,
                rented: 0,
                sold: 0,
                stored: 0,
                maintenance: 0
            };

            instruments.forEach(instrument => {
                if (statusCounts.hasOwnProperty(instrument.status)) {
                    statusCounts[instrument.status]++;
                }
            });

            // Create chart
            if (instrumentChartInstance.current) {
                instrumentChartInstance.current.destroy();
            }

            instrumentChartInstance.current = new Chart(instrumentChartRef.current, {
                type: 'doughnut',
                data: {
                    labels: ['Available', 'Rented', 'Sold', 'Stored', 'Maintenance'],
                    datasets: [{
                        data: [
                            statusCounts.available,
                            statusCounts.rented,
                            statusCounts.sold,
                            statusCounts.stored,
                            statusCounts.maintenance
                        ],
                        backgroundColor: [
                            '#28a745',
                            '#007bff',
                            '#dc3545',
                            '#6c757d',
                            '#ffc107'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        title: {
                            display: true,
                            text: 'Instruments by Status'
                        }
                    }
                }
            });
        }
    };

    const createRevenueChart = (orders) => {
        if (revenueChartRef.current) {
            // Group orders by month
            const monthlyRevenue = {};

            orders.forEach(order => {
                const date = new Date(order.order_date);
                const month = date.toLocaleString('default', { month: 'short' });

                if (!monthlyRevenue[month]) {
                    monthlyRevenue[month] = 0;
                }

                monthlyRevenue[month] += parseFloat(order.grand_total);
            });

            // Create chart
            if (revenueChartInstance.current) {
                revenueChartInstance.current.destroy();
            }

            const months = Object.keys(monthlyRevenue);
            const revenue = Object.values(monthlyRevenue);

            revenueChartInstance.current = new Chart(revenueChartRef.current, {
                type: 'bar',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Revenue',
                        data: revenue,
                        backgroundColor: '#007bff'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Monthly Revenue'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function (value) {
                                    return '$' + value;
                                }
                            }
                        }
                    }
                }
            });
        }
    };

    if (loading) {
        return <Loader />;
    }

    return (
        <div className="container-fluid py-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h1 className="h3">Dashboard</h1>
                <div>
                    <span className="text-muted me-2">Welcome,</span>
                    <span className="fw-bold">{user?.first_name} {user?.last_name}</span>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="row mb-4">
                <div className="col-md-6 col-lg-3 mb-3">
                    <div className="stat-card">
                        <div className="stat-card-title">Total Instruments</div>
                        <div className="stat-card-value">{stats.totalInstruments}</div>
                        <div className="stat-card-icon">
                            <i className="fas fa-microscope"></i>
                        </div>
                    </div>
                </div>

                <div className="col-md-6 col-lg-3 mb-3">
                    <div className="stat-card">
                        <div className="stat-card-title">Available Instruments</div>
                        <div className="stat-card-value">{stats.availableInstruments}</div>
                        <div className="stat-card-icon">
                            <i className="fas fa-check-circle"></i>
                        </div>
                    </div>
                </div>

                <div className="col-md-6 col-lg-3 mb-3">
                    <div className="stat-card">
                        <div className="stat-card-title">Total Orders</div>
                        <div className="stat-card-value">{stats.totalOrders}</div>
                        <div className="stat-card-icon">
                            <i className="fas fa-shopping-cart"></i>
                        </div>
                    </div>
                </div>

                <div className="col-md-6 col-lg-3 mb-3">
                    <div className="stat-card">
                        <div className="stat-card-title">Total Revenue</div>
                        <div className="stat-card-value">${stats.revenue.toFixed(2)}</div>
                        <div className="stat-card-icon">
                            <i className="fas fa-dollar-sign"></i>
                        </div>
                    </div>
                </div>
            </div>

            {/* Charts */}
            <div className="row mb-4">
                <div className="col-md-6 mb-4">
                    <div className="dashboard-widget">
                        <div className="dashboard-widget-title">Instrument Status</div>
                        <div style={{ height: '300px' }}>
                            <canvas ref={instrumentChartRef}></canvas>
                        </div>
                    </div>
                </div>

                <div className="col-md-6 mb-4">
                    <div className="dashboard-widget">
                        <div className="dashboard-widget-title">Revenue Overview</div>
                        <div style={{ height: '300px' }}>
                            <canvas ref={revenueChartRef}></canvas>
                        </div>
                    </div>
                </div>
            </div>

            {/* Recent Orders */}
            <div className="row">
                <div className="col-12">
                    <div className="dashboard-widget">
                        <div className="d-flex justify-content-between align-items-center mb-3">
                            <div className="dashboard-widget-title mb-0">Recent Orders</div>
                            <Link to="/orders" className="btn btn-sm btn-primary">
                                View All
                            </Link>
                        </div>

                        <div className="table-responsive">
                            <table className="table">
                                <thead>
                                    <tr>
                                        <th>Order #</th>
                                        <th>Client</th>
                                        <th>Type</th>
                                        <th>Date</th>
                                        <th>Amount</th>
                                        <th>Status</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {recentOrders.length > 0 ? (
                                        recentOrders.map(order => (
                                            <tr key={order.id}>
                                                <td>{order.order_number}</td>
                                                <td>{order.client_details?.hospital_name || 'N/A'}</td>
                                                <td>
                                                    {order.order_type === 'sale' && <span className="badge bg-success">Sale</span>}
                                                    {order.order_type === 'rental' && <span className="badge bg-primary">Rental</span>}
                                                    {order.order_type === 'storage' && <span className="badge bg-secondary">Storage</span>}
                                                </td>
                                                <td>{new Date(order.order_date).toLocaleDateString()}</td>
                                                <td>${parseFloat(order.grand_total).toFixed(2)}</td>
                                                <td>
                                                    {order.status === 'pending' && <span className="badge bg-warning">Pending</span>}
                                                    {order.status === 'confirmed' && <span className="badge bg-info">Confirmed</span>}
                                                    {order.status === 'processing' && <span className="badge bg-primary">Processing</span>}
                                                    {order.status === 'completed' && <span className="badge bg-success">Completed</span>}
                                                    {order.status === 'cancelled' && <span className="badge bg-danger">Cancelled</span>}
                                                </td>
                                                <td>
                                                    <Link to={`/orders/${order.id}`} className="btn btn-sm btn-outline-primary">
                                                        View
                                                    </Link>
                                                </td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan="7" className="text-center">No recent orders found</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard; 