import React, {useContext} from "react";
import {FormContext} from "../../../context/FormProvider";

const FormErrors = () => {
    const {formErrors} = useContext(FormContext);

    return (
        <React.Fragment>
            {formErrors && formErrors.hasOwnProperty("non_field_errors") &&
                <ul className="errors-list">
                    {formErrors["non_field_errors"].map((error, index) =>
                        <li className="error" key={index}>{error}</li>
                    )}
                </ul>
            }
        </React.Fragment>
    );
};

export default FormErrors;