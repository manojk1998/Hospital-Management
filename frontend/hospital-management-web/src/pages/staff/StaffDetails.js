import React from 'react';
import { useParams } from 'react-router-dom';

const StaffDetails = () => {
    const { id } = useParams();

    return (
        <div className="container py-4">
            <h1 className="mb-4">Staff Details</h1>
            <div className="card">
                <div className="card-body">
                    <p className="text-center">Details for staff ID: {id} will be displayed here.</p>
                </div>
            </div>
        </div>
    );
};

export default StaffDetails; 