import React, {useContext, useEffect, useState} from 'react';
import {useNavigate} from "react-router-dom";
import {AuthContext, UserContext} from "../../context/auth";
import userService from "../../services/user";
import InstituteService from "../../services/institute";
import {LoadingContext} from "../../context/base";

const AuthRoute = ({children}) => {
    const {setIsAuth} = useContext(AuthContext);
    const {setIsLoading} = useContext(LoadingContext);
    const [userData, setUserData] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        const getUserData = async () => {
            setIsLoading(true);

            const userServ = new userService();
            const userResponse = await userServ.getUserData();

            if (!userResponse.success) {
                setIsLoading(false);
                navigate("/accounts/login/");
                return;
            }

            const instituteServ = new InstituteService();
            const instituteResponse = await instituteServ.getById(userResponse.data.institute);

            setUserData({...userResponse.data, institute: instituteResponse.data});
            setIsAuth(userResponse.success && instituteResponse.success);
            setIsLoading(false);

            if (!userResponse.success && instituteResponse.success) navigate("/accounts/login/");
        };

        getUserData();
    }, [navigate]);

    return (
        <UserContext.Provider value={{userData, setUserData}}>
            {children}
        </UserContext.Provider>
    );
};

export default AuthRoute;