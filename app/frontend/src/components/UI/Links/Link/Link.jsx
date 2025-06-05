import React from "react";
import styles from "../Link.module.css";

const Link = ({children, className, ...props}) => {
    const linkClasses = [styles.link, className && className.split(" ")];

    return (
        <a className={linkClasses.join(" ")} {...props}>
            {children}
        </a>
    );
};

export default Link;