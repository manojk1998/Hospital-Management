import React from 'react';

const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="footer">
            <div className="container text-center">
                <span>
                    &copy; {currentYear} Hospital Instrument Management System. All rights reserved.
                </span>
            </div>
        </footer>
    );
};

export default Footer; 