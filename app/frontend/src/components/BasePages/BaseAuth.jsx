import React, {useContext} from "react";
import "../../styles/pages/auth.css";
import {LoadingContext} from "../../context/auth";
import Spinner from "../Spinner/Spinner";

const BaseAuth = ({children}) => {
    const {isPageLoading, setIsPageLoading} = useContext(LoadingContext);

    return (
        <section className="auth">
            <div className="container auth__container flex">
                {isPageLoading ? <Spinner/> : children}
            </div>
        </section>
    );
};

export default BaseAuth;