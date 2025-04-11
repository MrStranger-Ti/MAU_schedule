import React, {useContext, useEffect, useState} from "react";
import {LoadingContext} from "../../context/auth";

const Input = ({hasErrors, labelText, onChange, id, ...props}) => {
    const {isPageLoading, setIsPageLoading} = useContext(LoadingContext);

    const [hasInputError, setHasInputError] = useState(null);
    const [classes, setClasses] = useState(["config-input", "form-control"]);

    useEffect(() => {
        if (!isPageLoading) setHasInputError(hasErrors)
    }, [isPageLoading]);

    useEffect(() => {
        if (hasInputError) {
            setClasses([...classes, "error-input"]);
        } else {
            setClasses([...classes].filter((el) => el !== "error-input"));
        }
    }, [hasInputError]);

    const handleOnchange = (e) => {
        setHasInputError(false);
        onChange(e);
    }

    return (
        <div className="form-floating">
            <input
                className={[...classes].join(" ")}
                onChange={handleOnchange}
                id={id}
                {...props}
            />
            <label htmlFor={id}>{labelText}</label>
        </div>
    );
};

export default Input;