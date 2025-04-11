import React, {useContext} from "react";
import "../../styles/pages/auth.css";
import {LoadingContext} from "../../context/auth";
import Spinner from "../Spinner/Spinner";
import Main from "./Main";

const BaseAuth = ({children}) => {
    const {isPageLoading, setIsPageLoading} = useContext(LoadingContext);

    return (
        <Main>
            <section className="auth">
                <div className="container auth__container flex">
                    {isPageLoading ? <Spinner/> : children}
                </div>
            </section>
        </Main>
    );
};

export default BaseAuth;