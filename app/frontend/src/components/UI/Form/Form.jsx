import React, {useState} from "react";
import {FormContext} from "../../../context/UI";

const Form = ({
                  children,
                  formData,
                  request,
                  successful,
                  unsuccessful,
                  ...props
              }) => {
    const [formErrors, setFormErrors] = useState({});

    const onSubmit = async (e) => {
        e.preventDefault();

        const {success, data} = await request(formData);

        if (success) {
            if (typeof successful === "function") successful();
        } else {
            setFormErrors(data);
            if (typeof unsuccessful === "function") unsuccessful();
        }
    }

    return (
        <FormContext.Provider value={{formErrors, setFormErrors}}>
            <form onSubmit={onSubmit} {...props}>
                {children}
            </form>
        </FormContext.Provider>
    );
};

export default Form;