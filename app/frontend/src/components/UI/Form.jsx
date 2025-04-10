import React, {useContext, useState} from "react";
import {LoadingContext} from "../../context/auth";

const Form = ({
                  children,
                  request,
                  successful,
                  unsuccessful,
                  formData,
                  setFormData,
                  hasErrors,
                  setHasErrors,
                  classPrefix,
                  ...props
              }) => {
    const {isPageLoading, setIsPageLoading} = useContext(LoadingContext);

    const [dataErrors, setDataErrors] = useState({});

    const onSubmit = async (e) => {
        e.preventDefault();

        setIsPageLoading(true);

        const requestData = React.Children.toArray(children).reduce((res, element) => {
            if (element.type.name === "Input") {
                res[element.props.name] = element.props.value;
            }
            return res;
        }, {})

        const {success, data} = await request(requestData);

        if (success) {
            if (typeof successful === "function") successful();
        } else {
            setHasErrors(true);
            setDataErrors(data);
            if (typeof unsuccessful === "function") unsuccessful();
        }
        setIsPageLoading(false);
    }

    return (
        <form className={classPrefix + "__form flex"} onSubmit={onSubmit} {...props}>
            {dataErrors && dataErrors.hasOwnProperty("non_field_errors") &&
                <ul className="errors-list">
                    {dataErrors["non_field_errors"].map((error, index) =>
                        <li className={classPrefix + "__error"} key={index}>{error}</li>
                    )}
                </ul>
            }
            <div className={classPrefix + "__inputs-block flex"}>
                {React.Children.map(children, (child, index) =>
                    <React.Fragment>
                        {dataErrors && dataErrors.hasOwnProperty(child.props.name) &&
                            <ul>
                                {Object.entries(dataErrors[child.props.name]).map((error, index) =>
                                    <li className={classPrefix + "__error"} key={index}>{error}</li>
                                )}
                            </ul>
                        }
                        <div className={classPrefix + "__field-block"} key={index}>
                            {child}
                        </div>
                    </React.Fragment>
                )}
            </div>
            <button className={classPrefix + "__btn btn"} type="submit">Войти</button>
        </form>
    );
};

export default Form;