import React from "react";
import styles from "../Link.module.css";

const DarkLink = ({children, className, ...props}) => {
    const linkClasses = [styles.Link, styles.DarkLink, className && className.split(" ")];

    return (
        <a className={linkClasses.join(" ")} {...props}>
            {children}
        </a>
    );
};

export default DarkLink;