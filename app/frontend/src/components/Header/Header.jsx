import React from "react";
import {ReactComponent as MenuSVG} from "../../assets/svgs/icons/menu.svg";
import bearFace from "../../assets/images/logo/bear_face.png";
import {Link} from "react-router-dom";

const Header = () => {
    return (
        <header className="header">
            <div className="container header__container flex">
                <img src={bearFace} className="header__logo" alt="Логотип лицо медведя"/>
                <nav className="header__nav">
                    <ul className="header__nav-list flex">
                        <li className="header__nav-item"><Link to="/profile/" className="link header__nav-link">Профиль</Link></li>
                        <li className="header__nav-item"><Link to="/schedule/group/" className="link header__nav-link">...</Link></li>
                        <li className="header__nav-item"><Link to="/schedule/teacher-search/" className="link header__nav-link">Преподаватели</Link></li>
                    </ul>
                </nav>
                <form className="header__form" action="{% url 'mau_auth:logout' %}" method="post">
                    <button className="link header__form-link" type="submit">Выйти</button>
                </form>
                <nav className="header__menu">
                    <div className="dropdown">
                        <button className="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <MenuSVG/>
                        </button>
                        <ul className="dropdown-menu">
                            <li><a className="dropdown-item link dark-link" href="{% url 'profiles:profile' %}">Профиль</a></li>
                            <li><a className="dropdown-item link dark-link" href="{% url 'schedule:group_schedule' %}">...</a></li>
                            <li><a className="dropdown-item link dark-link" href="{% url 'schedule:teacher_search' %}">Преподаватели</a></li>
                            <li>
                                <form className="dropdown-item" action="{% url 'mau_auth:logout' %}" method="post">
                                    <button className="link dark-link header__form-link" type="submit">Выйти</button>
                                </form>
                            </li>
                        </ul>
                    </div>
                </nav>
            </div>
        </header>
    );
};

export default Header;