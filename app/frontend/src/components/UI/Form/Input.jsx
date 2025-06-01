import React, {useState} from "react";
import ErrorStyles from "./ErrorStyles";

const Input = ({className, onChange, name, value, ...props}) => {
    const [classes, setClasses] = useState(className ? className.split(" ") : []);
    const [hasInputErrors, setHasInputErrors] = useState(false);

    const handleOnchange = (e) => {
        setHasInputErrors(false);
        onChange(e);
    }

    return (
        <ErrorStyles
            inputName={name}
            hasInputErrors={hasInputErrors}
            setHasInputErrors={setHasInputErrors}
            classes={classes}
            setClasses={setClasses}
        >
            <input
                className={[...classes].join(" ")}
                onChange={handleOnchange}
                name={name}
                value={value !== null ? value : ""}
                {...props}
            />
        </ErrorStyles>
    );
};

export default Input;