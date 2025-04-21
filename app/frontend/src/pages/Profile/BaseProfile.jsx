import React, {useContext} from "react";
import "../../styles/pages/profile.css";
import Spinner from "../../components/Spinner/Spinner";
import Header from "../../components/Header/Header";
import Footer from "../../components/Footer/Footer";
import {AuthContext} from "../../context/auth";

const BaseProfile = ({children, title}) => {
    const {isCheckAuth} = useContext(AuthContext);

    return (
        <main>
            <Header/>
            <section className="profile">
                <div className={"profile__container container"}>
                    {isCheckAuth
                    ?
                    <Spinner/>
                    :
                    <React.Fragment>
                        <h1 className="profile__title title">
                            {title}
                        </h1>
                        <div className="profile__content flex">
                            {children}
                        </div>
                    </React.Fragment>
                }
                </div>
            </section>
            <Footer/>
        </main>
    );
};

export default BaseProfile;