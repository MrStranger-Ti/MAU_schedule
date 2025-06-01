import {createContext, useState} from "react";
import userService from "../../services/user";
import InstituteService from "../../services/institute";
import AuthService from "../../services/auth";

export const AuthContext = createContext(null);

const AuthProvider = ({children}) => {
    const [isAuth, setIsAuth] = useState(false);
    const [userData, setUserData] = useState({});
    const [isAuthCompleted, setIsAuthCompleted] = useState(false);

    const login = async () => {
        const userServ = new userService();
        const userResponse = await userServ.getUserData();

        if (!userResponse.success) {
            setIsAuth(false);
            return;
        }

        const instituteServ = new InstituteService();
        const instituteResponse = await instituteServ.getById(userResponse.data.institute);

        if (instituteResponse.success) {
            setUserData({...userResponse.data, institute: instituteResponse.data});
            setIsAuth(true);
        }
    }

    const logout = async () => {
        const service = new AuthService();
        const {success} = await service.deleteToken();
        if (success) setIsAuth(false);
    }

    return (
        <AuthContext.Provider value={{
            isAuth,
            setIsAuth,
            isAuthCompleted,
            setIsAuthCompleted,
            userData,
            setUserData,
            login,
            logout,
        }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;