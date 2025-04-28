import React from "react";
import {FormContext} from "../../../context/UI";

const Form = ({
                  children,
                  formErrors,
                  setFormErrors,
                  onSubmit,
                  ...props
              }, ref) => {
    return (
        <FormContext.Provider value={{formErrors, setFormErrors}}>
            <form ref={ref} onSubmit={onSubmit} {...props}>
                {children}
            </form>
        </FormContext.Provider>
    );
};

export default Form;