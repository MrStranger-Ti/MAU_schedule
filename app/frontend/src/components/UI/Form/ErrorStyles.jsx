import React, {useContext, useEffect} from "react";
import {FormContext} from "../../../context/UI";

const ErrorStyles = ({
                         children,
                         inputName,
                         hasInputErrors,
                         setHasInputErrors,
                         classes,
                         setClasses
                     }) => {
    const {formErrors} = useContext(FormContext);

    useEffect(() => {
        setHasInputErrors(
            formErrors.hasOwnProperty(inputName)
            || formErrors.hasOwnProperty("non_field_errors")
        )
    }, [formErrors]);

    useEffect(() => {
        if (hasInputErrors) {
            setClasses([...classes, "error-input"]);
        } else {
            setClasses([...classes].filter((el) => el !== "error-input"));
        }
    }, [hasInputErrors]);

    return (
        <React.Fragment>
            {children}
        </React.Fragment>
    );
};

export default ErrorStyles;