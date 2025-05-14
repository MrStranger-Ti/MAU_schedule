import React, {useEffect, useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import {Link, useParams} from "react-router-dom";
import AuthService from "../../../services/auth";
import {pagesPaths} from "../../../config";
import {LoadingContext} from "../../../context/LoadingProvider";
import {useAuth} from "../../../hooks/useAuth";

const RegisterConfirm = () => {
    const {uidb64, token} = useParams();

    const [isLoading, setIsLoading] = useState(true);
    const [successConfirm, setSuccessConfirm] = useState(false);

    const {isAuthCompleted} = useAuth(setIsLoading, {
        redirectAuthUser: true
    })

    useEffect(() => {
        const confirm = async () => {
            const service = new AuthService();
            const {success} = await service.registerConfirm({uidb64, token});

            if (success) {
                setSuccessConfirm(true);
            }
        }

        confirm();
    }, [isAuthCompleted]);

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseAuth>
                <Helmet>
                    <title>Подтверждение почты</title>
                </Helmet>
                <h1 className="auth__title">Подтверждение почты</h1>
                {successConfirm
                    ?
                    <p className="auth__descr">Почта успешно подтверждена!</p>
                    :
                    <p className="auth__descr">Не удалось подтвердить почту.</p>
                }
                <Link className="btn auth__btn" to={pagesPaths.accounts.login}>Войти</Link>
            </BaseAuth>
        </LoadingContext.Provider>
    );
};

export default RegisterConfirm;