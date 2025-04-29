import React, {useContext, useEffect} from "react";
import {AuthContext} from "../../context/auth";

const LogoutRoute = ({children}) => {
    const {isAuth, setIsAuth} = useContext(AuthContext);

    useEffect(() => {
        
    }, []);

    return (
        <React.Fragment>
            {children}
        </React.Fragment>
    );
};

export default LogoutRoute;