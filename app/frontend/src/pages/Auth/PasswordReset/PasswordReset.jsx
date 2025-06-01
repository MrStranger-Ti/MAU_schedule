import React, {useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import {Link} from "react-router-dom";
import BearFace from "../../../assets/images/logo/bear_face.png";
import PasswordResetForm from "./PasswordResetForm";
import {LoadingContext} from "../../../context/main/LoadingProvider";
import {useAuth} from "../../../hooks/auth/useAuth";
import {pagesPaths} from "../../../AppRoutes";

const PasswordReset = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [isSuccessEmailSent, setIsSuccessEmailSent] = useState(false);

    useAuth(setIsLoading, {
        redirectAuthUser: true
    })

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseAuth>
                <Helmet>
                    <title>Восстановление пароля</title>
                </Helmet>
                {!isSuccessEmailSent
                    ?
                    <React.Fragment>
                        <h1 className="auth__title">Восстановление пароля</h1>
                        <PasswordResetForm setIsSuccessEmailSent={setIsSuccessEmailSent}/>
                        <Link className="link dark-link" to={pagesPaths.accounts.login}>Войти</Link>
                    </React.Fragment>
                    :
                    <React.Fragment>
                        <img className="main-logo" src={BearFace} alt="логотип лицо медведя"/>
                        <p className="auth__descr">Письмо со ссылкой на сброс пароля успешно отправлено</p>
                        <Link className="btn auth__btn" to={pagesPaths.accounts.login}>Войти</Link>
                    </React.Fragment>
                }
            </BaseAuth>
        </LoadingContext.Provider>
    );
};

export default PasswordReset;