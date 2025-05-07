import {useContext, useState} from "react";
import userService from "../services/user";
import InstituteService from "../services/institute";
import {UserContext} from "../context/auth";
import AuthService from "../services/auth";

export const useAuth = () => {
    const [isAuth, setIsAuth] = useState(false);
    const {setUserData} = useContext(UserContext);

    const login = async () => {
        const userServ = new userService();
        const userResponse = await userServ.getUserData();

        if (!userResponse.success) return;

        const instituteServ = new InstituteService();
        const instituteResponse = await instituteServ.getById(userResponse.data.institute);

        setUserData({...userResponse.data, institute: instituteResponse.data});
        setIsAuth(instituteResponse.success);
    }

    const logout = async () => {
        const service = new AuthService();
        const {success} = await service.deleteToken();
        if (success) setIsAuth(false)
    }

    return {isAuth, login, logout};
}