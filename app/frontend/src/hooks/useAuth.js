import {useContext, useEffect, useState} from "react";
import {pagesPaths} from "../config";
import {useNavigate} from "react-router-dom";
import {AuthContext} from "../context/AuthProvider";

export const useAuth = (setIsLoading, {
    stopLoading = true,
    protect = false,
    redirectAuthUser = false
}) => {
    const navigate = useNavigate();
    const {isAuth, isAuthCompleted, setIsAuthCompleted, login} = useContext(AuthContext);
    const [isLogingCompleted, setIsLoginCompleted] = useState(false);

    useEffect(() => {
        const processLogin = async () => {
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
                setIsAuthCompleted(true);
                if (stopLoading) setIsLoading(false);
            }
        }
    }, [isLogingCompleted]);
}