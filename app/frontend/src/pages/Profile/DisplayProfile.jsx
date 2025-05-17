import React, {useContext} from "react";
import {Helmet} from "react-helmet";
import {AuthContext} from "../../context/AuthProvider";
import LoadingButton from "../../components/UI/Button/LoadingButton";

const DisplayProfile = ({isBtnLoading, loadUpdate}) => {
    const {userData} = useContext(AuthContext);

    return (
        <React.Fragment>
            <Helmet>
                <title>Профиль</title>
            </Helmet>
            <div className="row justify-content-between profile__lists-block flex-wrap gap-5">
                <div className="col profile__list-block">
                    <h2 className="profile__list-title">Личная информация</h2>
                    <ul className="profile__list">
                        <li className="profile__item"><span className="profile__item-name">ФИО: {userData.full_name}</span></li>
                        <li className="profile__item"><span className="profile__item-name">Email: {userData.email}</span></li>
                    </ul>
                </div>
                <div className="col profile__list-block">
                    <h2 className="profile__list-title">Студенческая информация</h2>
                    <ul className="profile__list">
                        <li className="profile__item"><span className="profile__item-name">Институт: {userData.institute && userData.institute.name}</span></li>
                        <li className="profile__item"><span className="profile__item-name">Курс: {userData.course}</span></li>
                        <li className="profile__item"><span className="profile__item-name">Группа: {userData.group}</span></li>
                    </ul>
                </div>
            </div>
            <div className="profile__btn-block">
                <LoadingButton
                    isLoading={isBtnLoading}
                    className="btn"
                    type="button"
                    onClick={loadUpdate}
                >
                    Редактировать
                </LoadingButton>
            </div>
        </React.Fragment>
    );
};

export default DisplayProfile;