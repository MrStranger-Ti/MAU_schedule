import React, {useContext} from "react";
import "../../styles/pages/schedule.css";
import {LoadingContext} from "../../context/base";
import Spinner from "../../components/Spinner/Spinner";
import Header from "../../components/Header/Header";
import Footer from "../../components/Footer/Footer";

const BaseSchedule = ({children}) => {
    const {isLoading} = useContext(LoadingContext);

    return (
        <main>
            <Header/>
            <section className="schedule">
                <div className="container schedule__container">
                    {isLoading
                        ?
                        <Spinner/>
                        :
                        <div className="schedule__content">
                            {children}
                        </div>
                    }
                </div>
            </section>
            <Footer/>
        </main>
    );
};

export default BaseSchedule;