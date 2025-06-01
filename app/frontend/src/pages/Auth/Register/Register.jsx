import React, {useContext, useEffect, useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import InstituteService from "../../../services/institute";
import {Link} from "react-router-dom";
import RegisterForm from "./RegisterForm";
import {useAuth} from "../../../hooks/auth/useAuth";
import {LoadingContext} from "../../../context/main/LoadingProvider";
import {NotificationContext} from "../../../context/main/NotificationProvider";
import {AuthContext} from "../../../context/main/AuthProvider";
import {pagesPaths} from "../../../AppRoutes";

const Register = () => {
    const {isAuthCompleted} = useContext(AuthContext);
    const {showNotification} = useContext(NotificationContext);
    const [isLoading, setIsLoading] = useState(true);
    const [institutes, setInstitutes] = useState([]);

    useAuth(setIsLoading, {
        redirectAuthUser: true
    });

    useEffect(() => {
        const loadPage = async () => {
            setIsLoading(true)

            const service = new InstituteService();
            const {success, data} = await service.getAll();
            if (success) {
                setInstitutes(data);
            } else {
                showNotification(data.detail, {error: true});
            }

            setIsLoading(false)
        }

        if (isAuthCompleted) loadPage();
    }, [isAuthCompleted]);

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseAuth>
                <Helmet>
                    <title>Регистрация</title>
                </Helmet>
                <h1 className="auth__title">Регистрация</h1>
                <React.Fragment>
                    <RegisterForm institutes={institutes}/>
                    <div className="auth__link-block">
                        <Link className="dark-link link" to={pagesPaths.accounts.login}>Войти</Link>
                    </div>
                </React.Fragment>
            </BaseAuth>
        </LoadingContext.Provider>
    );
};

export default Register;