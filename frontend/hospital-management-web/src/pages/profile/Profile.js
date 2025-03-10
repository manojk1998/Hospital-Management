import React from 'react';

const Profile = ({ user }) => {
    return (
        <div className="container py-4">
            <h1 className="mb-4">User Profile</h1>
            <div className="card">
                <div className="card-body">
                    {user ? (
                        <div>
                            <h5>Name: {user.first_name} {user.last_name}</h5>
                            <p>Email: {user.email}</p>
                            <p>Role: {user.role}</p>
                        </div>
                    ) : (
                        <p className="text-center">User profile information will be displayed here.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Profile; 