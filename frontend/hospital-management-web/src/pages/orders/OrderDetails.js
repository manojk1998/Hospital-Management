import React from 'react';
import { useParams } from 'react-router-dom';

const OrderDetails = () => {
    const { id } = useParams();

    return (
        <div className="container py-4">
            <h1 className="mb-4">Order Details</h1>
            <div className="card">
                <div className="card-body">
                    <p className="text-center">Details for order ID: {id} will be displayed here.</p>
                </div>
            </div>
        </div>
    );
};

export default OrderDetails; 