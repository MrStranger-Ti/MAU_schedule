import React, {useContext, useEffect} from "react";
import {FormContext} from "../../../context/FormProvider";

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
        if (formErrors) {
            setHasInputErrors(
                formErrors.hasOwnProperty(inputName)
                || formErrors.hasOwnProperty("non_field_errors")
            )
        }
    }, [formErrors]);

    useEffect(() => {
        if (formErrors) {
            if (hasInputErrors) {
                setClasses([...classes, "error-input"]);
            } else {
                setClasses([...classes].filter((el) => el !== "error-input"));
            }
        }
    }, [hasInputErrors]);

    return (
        <React.Fragment>
            {children}
        </React.Fragment>
    );
};

export default ErrorStyles;