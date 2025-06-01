import React from "react";
import styles from "../Button.module.css"

const Button = ({children, className = "", ...props}) => {
    const BtnClasses = [styles.Button, ...className.split(" ")];

    return (
        <button className={BtnClasses.join(" ")} {...props}>
            {children}
        </button>
    );
};

export default Button;