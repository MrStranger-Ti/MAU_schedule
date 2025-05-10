import React from "react";
import "../../styles/pages/schedule.css";
import Header from "../../components/Header/Header";
import Footer from "../../components/Footer/Footer";

const BaseSchedule = ({children}) => {
    return (
        <main>
            <Header/>
            <section className="schedule">
                <div className="container schedule__container">
                    {children}
                </div>
            </section>
            <Footer/>
        </main>
    );
};

export default BaseSchedule;