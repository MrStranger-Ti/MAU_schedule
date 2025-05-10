import React, {useContext, useEffect, useState} from "react";
import {LoadingContext} from "../../../context/base";
import ScheduleService from "../../../services/schedule";
import Spinner from "../../../components/Spinner/Spinner";
import ScheduleContent from "./ScheduleContent";
import {getFormattedDate} from "../../../utils/date";

const Schedule = () => {
    const {isLoading, setIsLoading} = useContext(LoadingContext);
    const [isScheduleLoading, setIsScheduleLoading] = useState(true);
    const [periods, setPeriods] = useState([]);
    const [currentPeriodValue, setCurrentPeriodValue] = useState("");
    const [isPeriodsLoaded, setIsPeriodLoaded] = useState(false);
    const [schedule, setSchedule] = useState({});
    const [isScheduleLoaded, setIsScheduleLoaded] = useState(false);

    const fetchSchedule = async () => {
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

    // Загрузка периодов расписания
    useEffect(() => {
        const loadPeriods = async () => {
            setIsLoading(true);

            if (periods.length === 0) {
                const service = new ScheduleService();
                const periodsResponse = await service.getPeriods();
                if (periodsResponse.success) {
                    setPeriods(
                        periodsResponse.data.map((period, index) =>
                            ({name: period, value: index})
                        )
                    );
                    setIsPeriodLoaded(true);
                }
            }
        }

        loadPeriods();
    }, []);

    // Загрузка расписания, используя текущий период
    useEffect(() => {
        const loadSchedule = async () => {
            if (Object.keys(schedule).length === 0) {
                await fetchSchedule();
                setIsScheduleLoaded(true);
            }
        }

        if (isPeriodsLoaded) loadSchedule();
    }, [isPeriodsLoaded]);

    // Установка текущего периода в Select
    useEffect(() => {
        if (isPeriodsLoaded) {
            if (Object.keys(schedule).length !== 0 && periods.length !== 0) {
                const isoWeekDay = getFormattedDate(Object.keys(schedule)[0]);
                const currentPeriodIndex = periods.findIndex(period => period.name.startsWith(isoWeekDay));
                setCurrentPeriodValue(periods[currentPeriodIndex].value);
            }

            setIsLoading(false);
        }
    }, [isScheduleLoaded]);

    return (
        <React.Fragment>
            {isLoading
                ?
                <Spinner/>
                :
                <ScheduleContent
                    fetchSchedule={fetchSchedule}
                    isScheduleLoading={isScheduleLoading}
                    schedule={schedule}
                    periods={periods}
                    currentPeriodValue={currentPeriodValue}
                    setCurrentPeriodValue={setCurrentPeriodValue}
                />
            }
        </React.Fragment>
    );
};

export default Schedule;