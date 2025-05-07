import React, {useContext, useEffect, useState} from "react";
import BaseSchedule from "../BaseSchedule";
import {UserContext} from "../../../context/auth";
import Select from "../../../components/UI/Form/Select";
import ScheduleService from "../../../services/schedule";
import {LoadingContext} from "../../../context/base";
import Form from "../../../components/UI/Form/Form";
import ScheduleTable from "../ScheduleTable";
import {Link} from "react-router-dom";
import {config} from "../../../config";
import Spinner from "../../../components/Spinner/Spinner";
import ButtonSpinner from "../../../components/Spinner/ButtonSpinner";
import Auth from "../../../components/Auth/Auth";

const Group = () => {
    const {setIsLoading} = useContext(LoadingContext);
    const {userData} = useContext(UserContext);
    const [isScheduleLoading, setIsScheduleLoading] = useState(true);
    const [periods, setPeriods] = useState([]);
    const [currentPeriodValue, setCurrentPeriodValue] = useState("");
    const [schedule, setSchedule] = useState({});

    const getSchedule = async () => {
        setIsScheduleLoading(true);

        const service = new ScheduleService();
        const scheduleResponse = await service.getGroupSchedule(
            currentPeriodValue ? periods[currentPeriodValue].name : {}
        );
        if (scheduleResponse.success) {
            setSchedule(scheduleResponse.data);
        } else {
            setSchedule({});
        }

        setIsScheduleLoading(false);
    }

    useEffect(() => {
        const loadPage = async () => {
            setIsLoading(true);

            const service = new ScheduleService();
            const periodsResponse = await service.getPeriods();
            if (periodsResponse.success) {
                setPeriods(
                    periodsResponse.data.map((period, index) =>
                        ({name: period, value: index})
                    )
                )
                await getSchedule();
            } else {
                setSchedule({});
            }

            setIsLoading(false);
        }

        loadPage();
    }, []);

    const onSubmit = async (e) => {
        e.preventDefault();
        await getSchedule();
    }

    return (
        <Auth stopLoading={false} protect={true}>
            <BaseSchedule>
                <div className="schedule__title-block flex">
                    <h1 className="schedule__title title">{userData.group}</h1>
                    <Form
                        className="schedule__form schedule__period-form flex"
                        onSubmit={onSubmit}
                    >
                        <Select
                            className="form-select"
                            onChange={(e) => setCurrentPeriodValue(e.target.value)}
                            name="period"
                            value={currentPeriodValue}
                            options={periods}
                            firstOption="Выберите период"
                        />
                        <button className="btn" type="submit" disabled={isScheduleLoading && true}>
                            {isScheduleLoading && <ButtonSpinner/>}
                            Найти
                        </button>
                    </Form>
                </div>
                {isScheduleLoading
                    ?
                    <Spinner/>
                    :
                    <React.Fragment>
                        {Object.keys(schedule).length > 0
                        ?
                        <ScheduleTable schedule={schedule}/>
                        :
                        <div className="schedule__info-block">
                            <p className="schedule__info">Расписание не найдено. Проверьте свои данные в профиле.</p>
                            <p className="schedule__info">
                                Также неполадки могут быть связаны с неработающим расписанием на <Link className="dark-link link" to={config.SCHEDULE_URL} target="_blank">сайте</Link> университета.
                            </p>
                        </div>
                        }
                    </React.Fragment>
                }
            </BaseSchedule>
        </Auth>
    );
};

export default Group;