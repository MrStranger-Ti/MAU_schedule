import {useContext, useEffect, useState} from "react";
import {PeriodsContext} from "../context/schedule/PeriodsProvider";
import {ScheduleContext} from "../context/schedule/ScheduleProvider";
import {NotesContext} from "../context/schedule/NotesProvider";
import {getFormattedDate} from "../utils/date";

const useSchedule = (dependenceState) => {
    const {
        fetchPeriods, isPeriodsLoaded,
        periods, setCurrentPeriodValue
    } = useContext(PeriodsContext);
    const {fetchSchedule, isScheduleLoaded, schedule} = useContext(ScheduleContext);
    const {fetchNotes, isNotesLoaded} = useContext(NotesContext);
    const [isScheduleDataLoaded, setIsScheduleDataLoaded] = useState(false);

    useEffect(() => {
        const loadPage = async () => {
            await fetchPeriods();
            await fetchSchedule();
            await fetchNotes();
        }

        if (dependenceState) loadPage();
    }, [dependenceState]);

    useEffect(() => {
        if (isPeriodsLoaded && isScheduleLoaded && isNotesLoaded) {
            const isoWeekDay = getFormattedDate(Object.keys(schedule)[0]);
            const currentPeriodIndex = periods.findIndex(period => period.name.startsWith(isoWeekDay));
            setCurrentPeriodValue(periods[currentPeriodIndex].value);
            setIsScheduleDataLoaded(true);
        }
    }, [isPeriodsLoaded, isScheduleLoaded, isNotesLoaded]);

    return {isScheduleDataLoaded};
}

export {useSchedule};