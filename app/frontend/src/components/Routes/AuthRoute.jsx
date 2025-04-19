import React, {useContext, useEffect, useState} from 'react';
import {useNavigate} from "react-router-dom";
import {AuthContext, UserContext} from "../../context/auth";
import userService from "../../services/user";
import instituteService from "../../services/institute";

const AuthRoute = ({children}) => {
    const {setIsAuth, setIsCheckAuth} = useContext(AuthContext);
    const [userData, setUserData] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        const getUserData = async () => {
            setIsCheckAuth(true);

            const userServ = new userService();
            const userResponse = await userServ.getUserData();

            if (!userResponse.success) {
                setIsCheckAuth(false);
                navigate("/accounts/login/");
                return;
            }

            const instituteServ = new instituteService();
            const instituteResponse = await instituteServ.getById(userResponse.data.institute);

            setUserData({...userResponse.data, institute: instituteResponse.data});
            setIsAuth(userResponse.success && instituteResponse.success);
            setIsCheckAuth(false);

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