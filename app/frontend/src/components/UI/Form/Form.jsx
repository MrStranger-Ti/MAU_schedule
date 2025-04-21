import React from "react";
import {FormContext} from "../../../context/UI";

const Form = ({
                  children,
                  formErrors,
                  setFormErrors,
                  onSubmit,
                  ...props
              }) => {
    return (
        <FormContext.Provider value={{formErrors, setFormErrors}}>
            <form onSubmit={onSubmit} {...props}>
                {children}
            </form>
        </FormContext.Provider>
    );
};

export default Form;