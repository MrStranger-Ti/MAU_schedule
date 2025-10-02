import React, {useContext, useEffect, useState} from "react";
import {ReactComponent as MenuSVG} from "../../assets/icons/menu.svg";
import bearFace from "../../assets/images/logo/bear_face.png";
import {useNavigate} from "react-router-dom";
import {LoadingContext} from "../../context/main/LoadingProvider";
import {AuthContext} from "../../context/main/AuthProvider";
import {pagesPaths} from "../../AppRoutes";
import baseStyles from "../../styles/base/Base.module.css";
import styles from "./Header.module.css";
import RouterLink from "../UI/Links/RouterLink/RouterLink";
import ButtonLink from "../UI/Links/ButtonLink/ButtonLink";
import {Dropdown} from "react-bootstrap";
import Button from "../UI/Buttons/Button/Button";
import DarkLink from "../UI/Links/DarkLink/DarkLink";
import DarkButtonLink from "../UI/Links/DarkButtonLink/DarkButtonLink";

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
        <header className={styles.header}>
            <div className={`${baseStyles.container} ${styles.container}`}>
                <img src={bearFace} className={styles.logo} alt="Логотип лицо медведя"/>
                <nav className={styles.nav}>
                    <ul className={styles.navList}>
                        <li><RouterLink to={pagesPaths.accounts.profile}>Профиль</RouterLink></li>
                        <li><RouterLink to={pagesPaths.schedule.group}>Группа</RouterLink></li>
                        <li><RouterLink to={pagesPaths.schedule.teacherSearch}>Преподаватели</RouterLink></li>
                    </ul>
                </nav>
                <ButtonLink className={styles.logoutButton} onClick={onClickLogout} type="button">Выйти</ButtonLink>
                <nav className={styles.menu}>
                    <Dropdown>
                        <Dropdown.Toggle variant="success" as="div">
                            <Button type="button">
                                <MenuSVG/>
                            </Button>
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item as="div">
                                <DarkLink href={pagesPaths.accounts.profile}>Профиль</DarkLink>
                            </Dropdown.Item>
                            <Dropdown.Item as="div">
                                <DarkLink href={pagesPaths.schedule.group}>Группа</DarkLink>
                            </Dropdown.Item>
                            <Dropdown.Item as="div">
                                <DarkLink href={pagesPaths.schedule.teacherSearch}>Преподаватели</DarkLink>
                            </Dropdown.Item>
                            <Dropdown.Item as="div">
                                <DarkButtonLink onClick={onClickLogout} type="button">Выйти</DarkButtonLink>
                            </Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                </nav>
            </div>
        </header>
    );
};

export default Header;