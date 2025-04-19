import React, {useState} from "react";
import ErrorStyles from "./ErrorStyles";

const Select = ({className, value, options, onChange, name, ...props}) => {
    const [classes, setClasses] = useState(className.split(" "));
    const [hasInputErrors, setHasInputErrors] = useState(false);

    const handleOnchange = (e) => {
        setHasInputErrors(false);
        onChange(e);
    }

    return (
        <ErrorStyles
            hasInputErrors={hasInputErrors}
            setHasInputErrors={setHasInputErrors}
            classes={className}
            setClasses={setClasses}
        >
            <select
                className={[...classes].join(" ")}
                onChange={handleOnchange}
                {...props}
            />
        </ErrorStyles>
    );
};

export default Select;