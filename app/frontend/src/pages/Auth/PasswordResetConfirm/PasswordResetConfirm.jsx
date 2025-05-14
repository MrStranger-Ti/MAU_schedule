import React, {useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import {Link} from "react-router-dom";
import BearFace from "../../../assets/images/logo/bear_face.png";
import {pagesPaths} from "../../../config";
import PasswordResetConfirmForm from "./PasswordResetConfirmForm";
import {LoadingContext} from "../../../context/LoadingProvider";
import {useAuth} from "../../../hooks/useAuth";

const PasswordResetConfirm = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [isSuccessPasswordChanged, setIsSuccessPasswordChanged] = useState(false);

    useAuth(setIsLoading, {
        redirectAuthUser: true
    })

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseAuth>
                <Helmet>
                    <title>Изменение пароля</title>
                </Helmet>
                {!isSuccessPasswordChanged
                    ?
                    <React.Fragment>
                        <h1 className="auth__title">Изменение пароля</h1>
                        <PasswordResetConfirmForm setIsSuccessPasswordChanged={setIsSuccessPasswordChanged}/>
                        <Link className="link dark-link" to={pagesPaths.accounts.login}>Войти</Link>
                    </React.Fragment>
                    :
                    <React.Fragment>
                        <img className="main-logo" src={BearFace} alt="логотип лицо медведя"/>
                        <p className="auth__descr">Пароль успешно изменен</p>
                        <Link className="btn auth__btn" to={pagesPaths.accounts.login}>Войти</Link>
                    </React.Fragment>
                }
            </BaseAuth>
        </LoadingContext.Provider>
    );
};

export default PasswordResetConfirm;