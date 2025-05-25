import React, {useContext, useEffect, useState} from "react";
import {ScheduleContext} from "../../context/schedule/ScheduleProvider";
import {LoadingContext} from "../../context/LoadingProvider";
import {AuthContext} from "../../context/AuthProvider";
import {PeriodsContext} from "../../context/schedule/PeriodsProvider";
import {NotesContext} from "../../context/schedule/NotesProvider";
import {getFormattedDate} from "../../utils/date";
import Spinner from "../Spinner/Spinner";
import ScheduleTables from "./Tables/ScheduleTables";
import TitleBlock from "./Content/TitleBlock/TitleBlock";

const Schedule = () => {
    const {isLoading, setIsLoading} = useContext(LoadingContext);
    const {isAuthCompleted} = useContext(AuthContext);
    const {
        fetchPeriods,
        periods,
        currentPeriodValue,
        setCurrentPeriodValue
    } = useContext(PeriodsContext);
    const {fetchSchedule, schedule, isScheduleLoading} = useContext(ScheduleContext);
    const {fetchNotes} = useContext(NotesContext);
    const [isLoadedData, setIsLoadedData] = useState(false);

    useEffect(() => {
        const loadPage = async () => {
            setIsLoading(true);

            await fetchPeriods();
            await fetchSchedule();
            await fetchNotes();

            setIsLoadedData(true);
        }

        if (isAuthCompleted) loadPage();
    }, [isAuthCompleted]);

    useEffect(() => {
        if (isLoadedData) {
            if (
                currentPeriodValue === ""
                && Object.keys(schedule).length > 0
                && Object.keys(periods).length > 0
            ) {
                const isoWeekDay = getFormattedDate(Object.keys(schedule)[0]);
                const currentPeriodIndex = periods.findIndex(period => period.name.startsWith(isoWeekDay));
                setCurrentPeriodValue(periods[currentPeriodIndex].value);
            }
            setIsLoading(false);
        }
    }, [isLoadedData]);

    return (
        <React.Fragment>
            {isLoading
                ?
                <Spinner/>
                :
                <div className="schedule__content">
                    <TitleBlock/>
                    {isScheduleLoading
                        ?
                        <Spinner/>
                        :
                        <ScheduleTables/>
                    }
                </div>
            }
        </React.Fragment>
    );
};

export default Schedule;