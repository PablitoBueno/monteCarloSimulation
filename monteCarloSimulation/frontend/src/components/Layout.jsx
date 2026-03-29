import React from 'react';

const Layout = ({ children }) => {
    return (
        <div className="container">
            <h1>Monte Carlo Simulation Configuration</h1>
            {children}
        </div>
    );
};

export default Layout;