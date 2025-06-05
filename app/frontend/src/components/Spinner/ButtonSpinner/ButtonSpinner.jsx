import React from "react";
import {Spinner} from "react-bootstrap";

const ButtonSpinner = ({...props}) => {
    return (
        <Spinner
            role="status"
            aria-hidden="true"
            {...props}
        >
        </Spinner>
    );
};

export default ButtonSpinner;