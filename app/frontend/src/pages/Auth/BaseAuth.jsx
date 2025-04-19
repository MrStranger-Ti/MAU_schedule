import React, {useContext} from "react";
import "../../styles/pages/auth.css";
import Spinner from "../../components/Spinner/Spinner";
import {AuthContext} from "../../context/auth";

const BaseAuth = ({children, isLoading}) => {
    const {isCheckAuth} = useContext(AuthContext);

    return (
        <main>
            <section className="auth">
                <div className="container auth__container flex">
                    {isCheckAuth || isLoading ? <Spinner/> : children}
                </div>
            </section>
        </main>
    );
};

export default BaseAuth;