import React from 'react';
import styles from "../Link.module.css";
import {Link} from "react-router-dom";

const RouterDarkLink = ({children, className, ...props}) => {
    const linkClasses = [styles.link, styles.darkLink, className && className.split(" ")];

    return (
        <Link className={linkClasses.join(" ")} {...props}>
            {children}
        </Link>
    );
};

export default RouterDarkLink;