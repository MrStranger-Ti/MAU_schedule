import React from "react";
import {Link} from "react-router-dom";
import {Helmet} from "react-helmet";
import BaseAuth from "../BaseAuth";
import {pagesPaths} from "../../../config";
import LoginForm from "./LoginForm";

const Login = () => {
    return (
        <BaseAuth>
            <Helmet>
                <title>Вход</title>
            </Helmet>
            <h1 className="auth__title">Вход</h1>
            <LoginForm/>
            <Link className="dark-link link" to={pagesPaths.accounts.register}>Регистрация</Link>
            <Link className="dark-link link" to={pagesPaths.accounts.passwordReset}>Восстановить пароль</Link>
        </BaseAuth>
    );
};

export default Login;