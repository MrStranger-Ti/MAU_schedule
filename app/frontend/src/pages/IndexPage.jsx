import React, {useState} from "react";
import {Link} from "react-router-dom";
import bearFace from "../assets/images/logo/bear_face.png";
import "../styles/pages/index.css";
import {pagesPaths} from "../config";
import {useAuth} from "../hooks/useAuth";
import Spinner from "../components/Spinner/Spinner";
import {LoadingContext} from "../context/LoadingProvider";

const IndexPage = () => {
    const [isLoading, setIsLoading] = useState(true);
    useAuth(setIsLoading, {
        redirectAuthUser: true
    });

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <section className="hero">
                <div className="container hero__container flex">
                    {isLoading
                        ?
                        <Spinner/>
                        :
                        <React.Fragment>
                            <img src={bearFace} className="main-logo" alt="логотип лицо медведя"/>
                            <h1 className="hero__title">Расписание доступно только для учащихся МАУ</h1>
                            <Link to={pagesPaths.accounts.login} className="btn hero__btn">Войти</Link>
                            <Link to={pagesPaths.accounts.register} className="link dark-link">Регистрация</Link>
                        </React.Fragment>
                    }
                </div>
            </section>
        </LoadingContext.Provider>
    );
};

export default IndexPage;