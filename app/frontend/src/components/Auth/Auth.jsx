import React, {useContext, useEffect, useState} from "react";
import {useAuth} from "../../hooks/useAuth";
import {LoadingContext} from "../../context/base";
import {useLocation, useNavigate} from "react-router-dom";
import {pagesPaths} from "../../config";
import {AuthContext} from "../../context/auth";

const Auth = ({children, stopLoading = true, protect = false, redirectAuthUser = false}) => {
    const location = useLocation();
    const [currentLocation] = useState(location.pathname);
    const {setIsLoading} = useContext(LoadingContext);
    const {isAuth, login, logout} = useAuth();
    const [isLogingCompleted, setIsLoginCompleted] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const processLogin = async () => {
            setIsLoading(true);

            await login();
            setIsLoginCompleted(true);
        }

        processLogin();
    }, []);

    useEffect(() => {
        if (isLogingCompleted) {
            if (!isAuth && protect) {
                navigate(pagesPaths.accounts.login);
            } else if (isAuth && redirectAuthUser) {
                navigate(pagesPaths.schedule.group);
            } else {
                if (stopLoading) setIsLoading(false);
            }
        }
    }, [isAuth, isLogingCompleted]);

    useEffect(() => {
        if (currentLocation !== location.pathname) {
            if (stopLoading) setIsLoading(false);
        }
    }, [location]);

    return (
        <AuthContext.Provider value={{isAuth, login, logout}}>
            {children}
        </AuthContext.Provider>
    );
};

export default Auth;