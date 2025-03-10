import React from 'react';
import { useParams } from 'react-router-dom';

const InstrumentDetails = () => {
    const { id } = useParams();

    return (
        <div className="container py-4">
            <h1 className="mb-4">Instrument Details</h1>
            <div className="card">
                <div className="card-body">
                    <p className="text-center">Details for instrument ID: {id} will be displayed here.</p>
                </div>
            </div>
        </div>
    );
};

export default InstrumentDetails; 