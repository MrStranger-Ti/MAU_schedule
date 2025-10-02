import React from "react";
import linksStyles from "../Link.module.css";
import styles from "./DarkButtonLink.module.css";

const DarkButtonLink = ({children, className, ...props}) => {
    const buttonClasses = [
        linksStyles.link,
        styles.button,
        className && className.split(" ")
    ];

    return (
        <button className={buttonClasses.join(" ")} {...props}>
            {children}
        </button>
    );
};

export default DarkButtonLink;