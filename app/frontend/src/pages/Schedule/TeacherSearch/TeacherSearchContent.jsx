import React, {useContext, useEffect, useState} from "react";
import Form from "../../../components/UI/Form/Form";
import Input from "../../../components/UI/Form/Input";
import LoadingButton from "../../../components/UI/Buttons/LoadingButton/LoadingButton";
import {TeacherBookmarksContext} from "../../../context/schedule/TeacherBookmarksProvider";
import {LoadingContext} from "../../../context/main/LoadingProvider";
import {AuthContext} from "../../../context/main/AuthProvider";
import Spinner from "../../../components/Spinner/Spinner";
import TeacherBookmarksDisplay from "../../../components/Schedule/Content/TeacherBookmarks/TeacherBookmarksDisplay/TeacherBookmarksDisplay";
import ScheduleService from "../../../services/schedule";
import {NotificationContext} from "../../../context/main/NotificationProvider";
import TeachersLinksList from "./TeachersLinksList";

const TeacherSearchContent = () => {
    const {isAuthCompleted} = useContext(AuthContext);
    const {showNotification} = useContext(NotificationContext);
    const {isLoading, setIsLoading} = useContext(LoadingContext);
    const {fetchTeacherBookmarks} = useContext(TeacherBookmarksContext);
    const [teacherQuery, setTeacherQuery] = useState("");
    const [teachersKeys, setTeachersKeys] = useState([]);
    const [isTeachersKeysLoaded, setIsTeachersKeysLoaded] = useState(false);
    const [isBtnLoading, setIsBtnLoading] = useState(false);

    useEffect(() => {
        const loadPage = async () => {
            setIsLoading(true);
            await fetchTeacherBookmarks();
            setIsLoading(false);
        }
        if (isAuthCompleted) loadPage();
    }, [isAuthCompleted]);

    const handleOnSubmit = async (e) => {
        e.preventDefault();

        setIsBtnLoading(true);

        const service = new ScheduleService();
        const {success, data} = await service.getTeacherKeys(teacherQuery);
        if (success) {
            setTeachersKeys(data);
        } else {
            setTeachersKeys([]);
            showNotification(data.detail, {error: true});
        }

        setIsTeachersKeysLoaded(true);
        setIsBtnLoading(false);
    }

    return (
        <React.Fragment>
            {isLoading
                ?
                <Spinner/>
                :
                <React.Fragment>
                    <div className="schedule__title-block flex">
                        <div className="schedule__title-left-block flex">
                            <h1 className="schedule__title title">Преподаватели</h1>
                            <TeacherBookmarksDisplay/>
                        </div>
                        <Form
                            className="schedule__form schedule__teacher-searching-form flex"
                            onSubmit={handleOnSubmit}
                        >
                            <Input
                                className="form-control"
                                onChange={(e) => setTeacherQuery(e.target.value)}
                                name="query"
                                value={teacherQuery}
                                type="text"
                                placeholder="ФИО преподавателя"
                                required
                            />
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
                        {isTeachersKeysLoaded
                            ?
                            <TeachersLinksList teachersKeys={teachersKeys}/>
                            :
                            <div className="schedule__info-block">
                                <p className="schedule__info">Найти преподавателя можно по Фамилии, Имени или Отчеству.</p>
                                <p className="schedule__info">Вы также можете посмотреть расписание на <a className="dark-link link" href="{{ original_schedule_url }}" target="_blank">сайте</a> университета.</p>
                            </div>
                        }
                    </div>
                </React.Fragment>
            }
        </React.Fragment>
    )
};

export default TeacherSearchContent;