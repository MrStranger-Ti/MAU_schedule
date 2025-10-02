import React from "react";
import BearBody from  "../../assets/images/logo/bear_body.png";
import {config} from "../../config";
import {pagesPaths} from "../../AppRoutes";
import RouterLink from "../UI/Links/RouterLink/RouterLink";
import baseStyles from "../../styles/base/Base.module.css";
import styles from "./Footer.module.css";
import Link from "../UI/Links/Link/Link";

const Footer = () => {
    return (
        <footer className={styles.footer}>
            <div className={`${baseStyles.container} ${styles.container}`}>
                <img className={styles.logo} src={BearBody} alt="медведь"/>
                <div className={styles.content}>
                    <nav>
                        <p className={styles.title}>Навигация</p>
                        <ul>
                            <li><RouterLink to={pagesPaths.accounts.profile}>Профиль</RouterLink></li>
                            <li><RouterLink to={pagesPaths.schedule.group}>Группа</RouterLink></li>
                            <li><RouterLink to={pagesPaths.schedule.teacherSearch}>Преподаватели</RouterLink></li>
                        </ul>
                    </nav>
                    <div>
                        <p className={styles.title}>Контакты</p>
                        <ul>
                            <li><Link href={config.SCHEDULE_URL} target="_blank">Сайт МАУ</Link></li>
                            <li><Link href={config.DEVELOPER_URL} target="_blank">Разработчик</Link></li>
                        </ul>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;