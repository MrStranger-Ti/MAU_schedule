import React, {useEffect, useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import InstituteService from "../../../services/institute";
import {Link} from "react-router-dom";
import {pagesPaths} from "../../../config";
import RegisterForm from "./RegisterForm";
import {useAuth} from "../../../hooks/useAuth";
import {LoadingContext} from "../../../context/LoadingProvider";

const Register = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [isSuccessRegister, setIsSuccessRegister] = useState(false);
    const [institutes, setInstitutes] = useState([]);

    const {isAuthCompleted} = useAuth(setIsLoading, {
        protect: true
    });

    useEffect(() => {
        const loadPage = async () => {
            setIsLoading(true)

            const service = new InstituteService();
            const {success, data} = await service.getAll();
            if (success) setInstitutes(data);

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
                {!isSuccessRegister
                    ?
                    <React.Fragment>
                        <RegisterForm
                            institutes={institutes}
                            setIsSuccessRegister={setIsSuccessRegister}
                        />
                        <div className="auth__link-block">
                            <Link className="dark-link link" to={pagesPaths.accounts.login}>Войти</Link>
                        </div>
                    </React.Fragment>
                    :
                    <React.Fragment>
                        <p className="auth__descr">
                            Письмо отправлено. Перейдите по ссылке в письме, чтобы подтвердить почту.
                        </p>
                        <Link className="btn" to={pagesPaths.accounts.login}>Войти</Link>
                    </React.Fragment>
                }
            </BaseAuth>
        </LoadingContext.Provider>
    );
};

export default Register;