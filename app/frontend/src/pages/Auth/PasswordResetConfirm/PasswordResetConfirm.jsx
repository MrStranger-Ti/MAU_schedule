import React, {useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import {Link} from "react-router-dom";
import PasswordResetConfirmForm from "./PasswordResetConfirmForm";
import {LoadingContext} from "../../../context/main/LoadingProvider";
import {useAuth} from "../../../hooks/auth/useAuth";
import {pagesPaths} from "../../../AppRoutes";

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