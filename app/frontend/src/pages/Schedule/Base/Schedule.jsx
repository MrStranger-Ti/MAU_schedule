import React, {useEffect, useState} from "react";
import ScheduleService from "../../../services/schedule";
import Spinner from "../../../components/Spinner/Spinner";
import ScheduleContent from "./Content/ScheduleContent";
import {getFormattedDate} from "../../../utils/date";
import NoteService from "../../../services/note";
import ScheduleProvider from "../../../context/ScheduleProvider";

const Schedule = ({
                      scheduleName,
                      scheduleKey,
                      isLoading,
                      setIsLoading,
                      isAuthCompleted
                  }) => {
    const [isScheduleLoading, setIsScheduleLoading] = useState(true);
    const [isLoadedData, setIsLoadedData] = useState(false);
    const [periods, setPeriods] = useState([]);
    const [currentPeriodValue, setCurrentPeriodValue] = useState("");
    const [schedule, setSchedule] = useState({});
    const [notes, setNotes] = useState([]);

    const fetchSchedule = async () => {
        console.log("dad")
        const service = new ScheduleService();
        let getScheduleFunc = null;
        switch (scheduleName) {
            case "group":
                getScheduleFunc = service.getGroupSchedule;
                break;
            case "teacher":
                getScheduleFunc = service.getTeacherSchedule;
                break;
        }

        const scheduleResponse = await service.getGroupSchedule(
            currentPeriodValue ? periods[currentPeriodValue].name : {}
        );
        if (scheduleResponse.success) {
            setSchedule(scheduleResponse.data);
        } else {
            setSchedule({});
        }
    }

    useEffect(() => {
        const loadPeriods = async () => {
            const service = new ScheduleService();
            const periodsResponse = await service.getPeriods();
            if (periodsResponse.success) {
                setPeriods(
                    periodsResponse.data.map((period, index) =>
                        ({name: period, value: index})
                    )
                );
            }
        }

        const loadSchedule = async () => {
            setIsScheduleLoading(true);
            await fetchSchedule();
            setIsScheduleLoading(false);
        }

        const loadNotes = async () => {
            const service = new NoteService();
            const {success, data} = await service.getAll();
            if (success) setNotes(data.results);
        }

        const loadPage = async () => {
            setIsLoading(true);

            await loadPeriods();
            await loadSchedule();
            await loadNotes();

            setIsLoadedData(true);
        }

        if (isAuthCompleted) loadPage();
    }, [isAuthCompleted]);

    useEffect(() => {
        if (isLoadedData) {
            if (currentPeriodValue === "") {
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
                <ScheduleProvider
                    scheduleName={scheduleName}
                    scheduleKey={scheduleKey}
                    fetchSchedule={fetchSchedule}
                    isScheduleLoading={isScheduleLoading}
                    setIsScheduleLoading={setIsScheduleLoading}
                    schedule={schedule}
                    periods={periods}
                    currentPeriodValue={currentPeriodValue}
                    setCurrentPeriodValue={setCurrentPeriodValue}
                    notes={notes}
                    setNotes={setNotes}
                >
                    <ScheduleContent/>
                </ScheduleProvider>
            }
        </React.Fragment>
    );
};

export default Schedule;