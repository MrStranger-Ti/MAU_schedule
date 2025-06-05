import React from "react";
import styles from "../Button.module.css"

const Button = ({children, className = "", ...props}) => {
    const btnClasses = [styles.button, ...className.split(" ")];

    return (
        <button className={btnClasses.join(" ")} {...props}>
            {children}
        </button>
    );
};

export default Button;