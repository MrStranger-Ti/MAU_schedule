import React from "react";
import styles from "../Link.module.css";

const DarkLink = ({children, className, ...props}) => {
    const linkClasses = [styles.link, styles.darkLink, className && className.split(" ")];

    return (
        <a className={linkClasses.join(" ")} {...props}>
            {children}
        </a>
    );
};

export default DarkLink;