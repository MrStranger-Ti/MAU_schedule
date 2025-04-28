import React, {useEffect, useState} from "react";
import Spinner from "../../../components/Spinner/Spinner";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import {Link, useParams} from "react-router-dom";
import AuthService from "../../../services/auth";

const RegisterConfirm = () => {
    const {uidb64, token} = useParams();

    const [isPageLoading, setIsPageLoading] = useState(true);
    const [successConfirm, setSuccessConfirm] = useState(false);

    useEffect(() => {
        const confirm = async () => {
            const service = new AuthService();
            const {success} = await service.registerConfirm({uidb64, token});

            if (success) {
                setSuccessConfirm(true);
                setIsPageLoading(false);
            }
        }

        confirm();
    }, []);

    return (
        <BaseAuth>
            <Helmet>
                <title>Подтверждение почты</title>
            </Helmet>
            <h1 className="auth__title">Подтверждение почты</h1>
            {isPageLoading
                ?
                <Spinner/>
                :
                <React.Fragment>
                    {successConfirm
                        ?
                        <p className="auth__descr">Почта успешно подтверждена!</p>
                        :
                        <p className="auth__descr">Не удалось подтвердить почту.</p>
                    }
                </React.Fragment>
            }
            <Link className="btn auth__btn" to="/accounts/login/">Войти</Link>
        </BaseAuth>
    );
};

export default RegisterConfirm;