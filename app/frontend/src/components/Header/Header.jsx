import React, {useContext} from "react";
import {ReactComponent as MenuSVG} from "../../assets/svgs/icons/menu.svg";
import bearFace from "../../assets/images/logo/bear_face.png";
import {Link, useNavigate} from "react-router-dom";
import AuthService from "../../services/auth";
import {AuthContext} from "../../context/auth";

const Header = () => {
    const {setIsAuth} = useContext(AuthContext);

    const navigate = useNavigate();

    const logout = async (e) => {
        const service = new AuthService();
        const {success} = await service.logout();
        setIsAuth(false);
        if (success) navigate("/accounts/login/");
    }

    return (
        <header className="header">
            <div className="container header__container flex">
                <img src={bearFace} className="header__logo" alt="Логотип лицо медведя"/>
                <nav className="header__nav">
                    <ul className="header__nav-list flex">
                        <li className="header__nav-item"><Link className="link header__nav-link" to="/profile/">Профиль</Link></li>
                        <li className="header__nav-item"><Link className="link header__nav-link" to="/schedule/group/">Группа</Link></li>
                        <li className="header__nav-item"><Link className="link header__nav-link" to="/schedule/teacher-search/">Преподаватели</Link></li>
                    </ul>
                </nav>
                <button className="link header__form-link" onClick={logout} type="button">Выйти</button>
                <nav className="header__menu">
                    <div className="dropdown">
                        <button className="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <MenuSVG/>
                        </button>
                        <ul className="dropdown-menu">
                            <li><Link className="dropdown-item link dark-link" to="/profile/">Профиль</Link></li>
                            <li><Link className="dropdown-item link dark-link" to="/schedule/group/">Группа</Link></li>
                            <li><Link className="dropdown-item link dark-link" to="/schedule/teacher-search/">Преподаватели</Link></li>
                            <li><button className="link header__form-link" onClick={logout} type="button">Выйти</button></li>
                        </ul>
                    </div>
                </nav>
            </div>
        </header>
    );
};

export default Header;