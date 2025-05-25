import React, {useState} from 'react';
import {LoadingContext} from "../../../context/LoadingProvider";
import BaseSchedule from "../BaseSchedule";
import {useAuth} from "../../../hooks/useAuth";
import Form from "../../../components/UI/Form/Form";
import Input from "../../../components/UI/Form/Input";
import LoadingButton from "../../../components/UI/Button/LoadingButton";

const TeacherSearch = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [query, setQuery] = useState();
    const [isBtnLoading, setIsBtnLoading] = useState(false);

    useAuth(setIsLoading, {
        stopLoading: false,
        protect: true
    });

    const onSubmit = (e) => {
        e.preventDefault();

    }

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseSchedule>
                <div className="schedule__title-block flex">
                    <div className="schedule__title-left-block flex">
                        <h1 className="schedule__title title">Преподаватели</h1>
                        {/*<div className="schedule__options">*/}
                        {/*    {% include 'bookmarks/bookmarks.html' %}*/}
                        {/*</div>*/}
                    </div>
                    <Form
                        className="schedule__form schedule__teacher-searching-form flex"
                        onSubmit={onSubmit}
                    >
                        <div className="form-floating">
                            <Input
                                className="form-control"
                                onChange={(e) => setQuery(e.target.value)}
                                name="query"
                                value={query}
                                type="text"
                                id="floatingQuery"
                                placeholder="query"
                                required
                            />
                            <label htmlFor="floatingQuery">ФИО преподавателя</label>
                        </div>
                        <LoadingButton
                            isLoading={isBtnLoading}
                            className="btn schedule__search-btn"
                            type="submit"
                        >
                            Найти
                        </LoadingButton>
                    </Form>
                </div>
                <div className="schedule__teachers-list">
                    <div className="schedule__info-block">
                        <p className="schedule__info">Найти преподавателя можно по Фамилии, Имени или Отчеству.</p>
                        <p className="schedule__info">Вы также можете посмотреть расписание на <a className="dark-link link" href="{{ original_schedule_url }}" target="_blank">сайте</a> университета.</p>
                    </div>
                </div>
            </BaseSchedule>
        </LoadingContext.Provider>
    );
};

export default TeacherSearch;