import React, {useContext, useEffect, useState} from "react";
import {ReactComponent as MenuSVG} from "../../assets/svgs/icons/menu.svg";
import bearFace from "../../assets/images/logo/bear_face.png";
import {Link, useNavigate} from "react-router-dom";
import {LoadingContext} from "../../context/main/LoadingProvider";
import {AuthContext} from "../../context/main/AuthProvider";
import {pagesPaths} from "../../AppRoutes";

const Header = () => {
    const {isAuth, logout} = useContext(AuthContext);
    const {setIsLoading} = useContext(LoadingContext);
    const [isLogoutCompleted, setIsLogoutCompleted] = useState(false);
    const navigate = useNavigate();

    const onClickLogout = async () => {
        setIsLoading(true);

        await logout();

        setIsLogoutCompleted(true);
    }

    useEffect(() => {
        if (!isAuth && isLogoutCompleted) {
            setIsLoading(false);
            navigate(pagesPaths.accounts.login);
        }
    }, [isAuth, isLogoutCompleted]);

    return (
        <header className="header">
            <div className="container header__container flex">
                <img src={bearFace} className="header__logo" alt="Логотип лицо медведя"/>
                <nav className="header__nav">
                    <ul className="header__nav-list flex">
                        <li className="header__nav-item"><Link className="link header__nav-link" to={pagesPaths.accounts.profile}>Профиль</Link></li>
                        <li className="header__nav-item"><Link className="link header__nav-link" to={pagesPaths.schedule.group}>Группа</Link></li>
                        <li className="header__nav-item"><Link className="link header__nav-link" to={pagesPaths.schedule.teacherSearch}>Преподаватели</Link></li>
                    </ul>
                </nav>
                <button className="link header__form-link" onClick={onClickLogout} type="button">Выйти</button>
                <nav className="header__menu">
                    <div className="dropdown">
                        <button className="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <MenuSVG/>
                        </button>
                        <ul className="dropdown-menu">
                            <li><Link className="dropdown-item link dark-link" to={pagesPaths.accounts.profile}>Профиль</Link></li>
                            <li><Link className="dropdown-item link dark-link" to={pagesPaths.schedule.group}>Группа</Link></li>
                            <li><Link className="dropdown-item link dark-link" to={pagesPaths.schedule.teacherSearch}>Преподаватели</Link></li>
                            <li><button className="link header__form-link" onClick={onClickLogout} type="button">Выйти</button></li>
                        </ul>
                    </div>
                </nav>
            </div>
        </header>
    );
};

export default Header;