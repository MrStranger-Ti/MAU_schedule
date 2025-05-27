import React, {useContext} from "react";
import "../../styles/pages/auth.css";
import Spinner from "../../components/Spinner/Spinner";
import {LoadingContext} from "../../context/main/LoadingProvider";

const BaseAuth = ({children}) => {
    const {isLoading} = useContext(LoadingContext);

    return (
        <main>
            <section className="auth">
                <div className="container auth__container flex">
                    {isLoading ? <Spinner/> : children}
                </div>
            </section>
        </main>
    );
};

export default BaseAuth;