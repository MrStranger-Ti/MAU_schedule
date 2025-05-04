import React, {useContext} from "react";
import {AuthContext} from "../../../context/auth";
import {Link, Navigate} from "react-router-dom";
import {Helmet} from "react-helmet";
import BaseAuth from "../BaseAuth";
import LoginForm from "./LoginForm";
import {pagesPaths} from "../../../config";

const Login = () => {
    const {isAuth} = useContext(AuthContext);

    return (
        <BaseAuth>
            <Helmet>
                <title>Вход</title>
            </Helmet>
            {isAuth
                ?
                <Navigate to={pagesPaths.accounts.profile}/>
                :
                <React.Fragment>
                    <h1 className="auth__title">Вход</h1>
                    <LoginForm/>
                    <Link className="dark-link link" to={pagesPaths.accounts.register}>Регистрация</Link>
                    <Link className="dark-link link" to={pagesPaths.accounts.passwordReset}>Восстановить пароль</Link>
                </React.Fragment>
            }
        </BaseAuth>
    );
};

export default Login;