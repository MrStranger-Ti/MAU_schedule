import React from 'react';

const BaseAuth = ({children}) => {
    return (
        <section className="auth">
            <div className="container auth__container flex">
                {children}
            </div>
        </section>
    );
};

export default BaseAuth;