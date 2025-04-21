import React from "react";
import {Link} from "react-router-dom";
import BearBody from  "../../assets/images/logo/bear_body.png";
import config from "../../config";

const Footer = () => {
    return (
        <footer className="footer">
            <div className="container footer__container flex">
                <img className="footer__logo" src={BearBody} alt="логотип тела медведя"/>
                <div className="footer__content flex">
                    <nav className="footer__nav">
                        <p className="footer__title">Навигация</p>
                        <ul className="footer__nav-list">
                            <li className="footer__nav-item"><Link to="#" className="footer__link link">Профиль</Link></li>
                            <li className="footer__nav-item"><Link to="#" className="footer__link link">Группа</Link></li>
                            <li className="footer__nav-item"><Link to="#" className="footer__link link">Преподаватели</Link></li>
                        </ul>
                    </nav>
                    <div className="footer__contacts">
                        <p className="footer__title">Контакты</p>
                        <ul className="footer__contacts-list">
                            <li className="footer__contacts-item"><Link to={config.SCHEDULE_URL} className="link" target="_blank">Сайт МАУ</Link></li>
                            <li className="footer__contacts-item"><Link to={config.DEVELOPER_URL} className="link" target="_blank">Разработчик</Link></li>
                        </ul>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;