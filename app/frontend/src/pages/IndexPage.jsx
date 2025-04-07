import React from "react";
import {Link} from "react-router-dom";
import bearFace from "../assets/images/logo/bear_face.png";
import "../styles/pages/index.css";

const IndexPage = () => {
    return (
        <section className="hero">
            <div className="container hero__container flex">
                <img src={bearFace} className="main-logo" alt="логотип лицо медведя"/>
                <h1 className="hero__title">Расписание доступно только для учащихся МАУ</h1>
                <Link to="/accounts/login/" className="btn hero__btn">Войти</Link>
                <Link to="/accounts/register/" className="link dark-link">Регистрация</Link>
            </div>
        </section>
    );
};

export default IndexPage;