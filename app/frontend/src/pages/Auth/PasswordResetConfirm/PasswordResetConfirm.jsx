import React, {useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import {Link} from "react-router-dom";
import {pagesPaths} from "../../../config";
import PasswordResetConfirmForm from "./PasswordResetConfirmForm";
import {LoadingContext} from "../../../context/LoadingProvider";
import {useAuth} from "../../../hooks/useAuth";

const PasswordResetConfirm = () => {
    const [isLoading, setIsLoading] = useState(true);

    useAuth(setIsLoading, {
        redirectAuthUser: true
    })

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseAuth>
                <Helmet>
                    <title>Изменение пароля</title>
                </Helmet>
                <h1 className="auth__title">Изменение пароля</h1>
                <PasswordResetConfirmForm/>
                <Link className="link dark-link" to={pagesPaths.accounts.login}>Войти</Link>
            </BaseAuth>
        </LoadingContext.Provider>
    );
};

export default PasswordResetConfirm;