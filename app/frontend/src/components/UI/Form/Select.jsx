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
            inputName={name}
            hasInputErrors={hasInputErrors}
            setHasInputErrors={setHasInputErrors}
            classes={classes}
            setClasses={setClasses}
        >
            <select
                className={[...classes].join(" ")}
                onChange={handleOnchange}
                name={name}
                value={value}
                {...props}
            >
                <option value="0">Выберите институт</option>
                {options.map((option, ind) =>
                    <option value={option.value} key={ind}>{option.name}</option>
                )}
            </select>
        </ErrorStyles>
    );
};

export default Select;