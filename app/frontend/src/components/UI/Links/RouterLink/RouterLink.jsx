import React from "react";
import styles from "../Link.module.css";
import {Link} from "react-router-dom";

const RouterLink = ({children, className, ...props}) => {
    const linkClasses = [styles.link, className && className.split(" ")];

    return (
        <Link className={linkClasses.join(" ")} {...props}>
            {children}
        </Link>
    );
};

export default RouterLink;