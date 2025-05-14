import React from "react";
import {FormContext} from "../../../context/FormProvider";

const Form = ({
                  children,
                  formErrors,
                  setFormErrors,
                  onSubmit,
                  ref,
                  ...props
              }) => {
    return (
        <FormContext.Provider value={{formErrors, setFormErrors}}>
            <form ref={ref} onSubmit={onSubmit} {...props}>
                {children}
            </form>
        </FormContext.Provider>
    );
};

export default Form;