import React, {useContext} from "react";
import {FormContext} from "../../../context/UI";

const InputErrors = ({inputName}) => {
    const {formErrors} = useContext(FormContext);

    return (
        <React.Fragment>
            {formErrors && formErrors.hasOwnProperty(inputName) &&
                <ul className="errors-list">
                    {formErrors[inputName].map((error, index) =>
                        <li className="error" key={index}>{error}</li>
                    )}
                </ul>
            }
        </React.Fragment>
    );
};

export default InputErrors;