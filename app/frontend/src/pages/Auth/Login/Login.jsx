import React, {useState} from "react";
import {Link} from "react-router-dom";
import {Helmet} from "react-helmet";
import BaseAuth from "../BaseAuth";
import LoginForm from "./LoginForm";
import {useAuth} from "../../../hooks/useAuth";
import {LoadingContext} from "../../../context/main/LoadingProvider";
import {pagesPaths} from "../../../AppRoutes";

const Login = () => {
    const [isLoading, setIsLoading] = useState(true);

    useAuth(setIsLoading, {
        redirectAuthUser: true
    })

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseAuth>
                <Helmet>
                    <title>Вход</title>
                </Helmet>
                <h1 className="auth__title">Вход</h1>
                <LoginForm/>
                <Link className="dark-link link" to={pagesPaths.accounts.register}>Регистрация</Link>
                <Link className="dark-link link" to={pagesPaths.accounts.passwordReset}>Восстановить пароль</Link>
            </BaseAuth>
        </LoadingContext.Provider>
    );
};

export default Login;