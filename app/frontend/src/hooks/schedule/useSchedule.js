import {useContext, useEffect, useState} from "react";
import {PeriodsContext} from "../../context/schedule/PeriodsProvider";
import {ScheduleContext} from "../../context/schedule/ScheduleProvider";
import {NotesContext} from "../../context/schedule/NotesProvider";
import {getFormattedDate} from "../../utils/date";

const useSchedule = (dependenceArray) => {
    const {
        fetchPeriods, isPeriodsLoaded, setIsPeriodsLoaded,
        periods, setCurrentPeriodValue
    } = useContext(PeriodsContext);
    const {
        fetchSchedule,
        isScheduleLoaded, setIsScheduleLoaded,
        schedule
    } = useContext(ScheduleContext);
    const {fetchNotes, isNotesLoaded, setIsNotesLoaded} = useContext(NotesContext);
    const [isScheduleDataLoaded, setIsScheduleDataLoaded] = useState(false);

    useEffect(() => {
        const loadPage = async () => {
            await fetchPeriods();
            await fetchSchedule();
            await fetchNotes();
        }

        if (dependenceArray.every(state => Boolean(state))) loadPage();
    }, dependenceArray);

    useEffect(() => {
        if (isPeriodsLoaded && isScheduleLoaded && isNotesLoaded) {
            const isoWeekDay = getFormattedDate(Object.keys(schedule)[0]);
            const currentPeriodIndex = periods.findIndex(period => period.name.startsWith(isoWeekDay));
            setCurrentPeriodValue(periods[currentPeriodIndex].value);
            setIsScheduleDataLoaded(true);
        }
    }, [isPeriodsLoaded, isScheduleLoaded, isNotesLoaded]);

    useEffect(() => {
        if (isScheduleDataLoaded) {
            setIsPeriodsLoaded(false);
            setIsScheduleLoaded(false);
            setIsNotesLoaded(false);
            setIsScheduleDataLoaded(false);
        }
    }, [isScheduleDataLoaded]);

    return {isScheduleDataLoaded};
}

export {useSchedule};