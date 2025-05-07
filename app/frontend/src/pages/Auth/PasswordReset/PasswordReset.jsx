import React, {useContext, useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import {Link} from "react-router-dom";
import Form from "../../../components/UI/Form/Form";
import InputErrors from "../../../components/UI/Form/InputErrors";
import Input from "../../../components/UI/Form/Input";
import {pagesPaths} from "../../../config";
import AuthService from "../../../services/auth";
import {LoadingContext} from "../../../context/base";
import BearFace from "../../../assets/images/logo/bear_face.png";
import Auth from "../../../components/Auth/Auth";
import PasswordResetForm from "./PasswordResetForm";

const PasswordReset = () => {
    const [isSuccessEmailSent, setIsSuccessEmailSent] = useState(false);

    return (
        <Auth redirectAuthUser={true}>
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
        </Auth>
    );
};

export default PasswordReset;