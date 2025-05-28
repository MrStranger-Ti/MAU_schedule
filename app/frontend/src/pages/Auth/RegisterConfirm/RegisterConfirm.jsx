import React, {useContext, useEffect, useState} from "react";
import BaseAuth from "../BaseAuth";
import {useNavigate, useParams} from "react-router-dom";
import AuthService from "../../../services/auth";
import {LoadingContext} from "../../../context/main/LoadingProvider";
import {useAuth} from "../../../hooks/useAuth";
import {NotificationContext} from "../../../context/main/NotificationProvider";
import {AuthContext} from "../../../context/main/AuthProvider";
import {pagesPaths} from "../../../AppRoutes";

const RegisterConfirm = () => {
    const {uidb64, token} = useParams();

    const {isAuthCompleted} = useContext(AuthContext);
    const {showNotification} = useContext(NotificationContext);
    const [isLoading, setIsLoading] = useState(true);
    const navigate = useNavigate();

    useAuth(setIsLoading, {
        redirectAuthUser: true
    })

    useEffect(() => {
        const confirm = async () => {
            const service = new AuthService();
            const {success} = await service.registerConfirm({uidb64, token});

            if (success) {
                showNotification("Почта успешно подтверждена");
            } else {
                showNotification("Не удалось подтвердить почту");
            }

            navigate(pagesPaths.accounts.login);
        }

        if (isAuthCompleted) confirm();
    }, [isAuthCompleted]);

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseAuth/>
        </LoadingContext.Provider>
    );
};

export default RegisterConfirm;