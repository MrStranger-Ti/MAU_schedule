import React from "react";

const Spinner = () => {
    return (
        <div className="spinner-block">
            <div className="spinner-border spinner-border-visible" role="status">
                <span className="visually-hidden"></span>
            </div>
        </div>
    );
};

export default Spinner;