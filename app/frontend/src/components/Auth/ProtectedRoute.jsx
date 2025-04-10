import React, {useContext, useEffect} from 'react';
import {useNavigate} from "react-router-dom";
import {AuthContext, LoadingContext} from "../../context/auth";

const ProtectedRoute = ({children}) => {
    const {isAuth, setIsAuth} = useContext(AuthContext);
    const {isPageLoading, setIsPageLoading} = useContext(LoadingContext);

    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuth && !isPageLoading) navigate("/accounts/login/");
    }, [isAuth, isPageLoading]);

    return (
        <React.Fragment>
            {children}
        </React.Fragment>
    );
};

export default ProtectedRoute;