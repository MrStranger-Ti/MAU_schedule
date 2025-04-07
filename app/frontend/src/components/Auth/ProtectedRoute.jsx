import React, {useContext, useEffect} from 'react';
import {Navigate} from "react-router-dom";
import {AuthContext} from "../../context/auth";
import AuthService from "../../services/auth";

const ProtectedRoute = ({children}) => {
    const {isAuth, setIsAuth, isLoading, setIsLoading} = useContext(AuthContext);

    useEffect(() => {
        const checkAuth = async () => {
            const service = new AuthService()
            const {success, data, error} = await service.isAuthenticated()
            setIsAuth(success)
            setIsLoading(false)
        };

        checkAuth();
    }, []);

    if (isLoading) {
        return <div>Loading...</div>
    }

    if (!isAuth) {
        return <Navigate to="/accounts/login/"/>
    }

    return (
        <AuthContext.Provider value={{isAuth, setIsAuth, isLoading, setIsLoading}}>
            {children}
        </AuthContext.Provider>
    );
};

export default ProtectedRoute;