import React, {useState} from "react";
import ErrorStyles from "../ErrorStyles";
import styles from "./Select.module.css";

const Select = ({className, onChange, name, value, options, firstOption, ...props}) => {
    const [classes, setClasses] = useState(
        ["form-select"].concat(className ? className.split(" ") : [])
    );
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
                <option className={styles.option} value="">
                    {firstOption || "Выберите"}
                </option>
                {options.map((option, ind) =>
                    <option
                        className={styles.option}
                        value={option.value}
                        key={ind}
                    >{option.name}</option>
                )}
            </select>
        </ErrorStyles>
    );
};

export default Select;