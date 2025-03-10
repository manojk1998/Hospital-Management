import React from 'react';

const Loader = ({ fullScreen = true }) => {
    if (fullScreen) {
        return (
            <div className="loader-container">
                <div className="loader"></div>
            </div>
        );
    }

    return (
        <div className="d-flex justify-content-center my-5">
            <div className="loader"></div>
        </div>
    );
};

export default Loader; 