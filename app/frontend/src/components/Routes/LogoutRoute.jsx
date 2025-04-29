import React, {useContext, useEffect} from "react";
import {AuthContext} from "../../context/auth";
import AuthService from "../../services/auth";
import {LoadingContext} from "../../context/base";

const LogoutRoute = ({children}) => {
    const {isAuth, setIsAuth} = useContext(AuthContext);
    const {setIsLoading} = useContext(LoadingContext);

    useEffect(() => {
        const logout = async () => {
            setIsLoading(true);

            const service = new AuthService();
            const {success} = await service.logout();
            if (success) {
                setIsAuth(false);
            }

            setIsLoading(false);
        }

        if (isAuth) logout();
    }, []);

    return (
        <React.Fragment>
            {children}
        </React.Fragment>
    );
};

export default LogoutRoute;