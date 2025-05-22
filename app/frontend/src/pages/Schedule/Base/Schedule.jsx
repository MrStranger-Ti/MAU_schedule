import React, {useContext, useEffect, useState} from "react";
import ScheduleService from "../../../services/schedule";
import Spinner from "../../../components/Spinner/Spinner";
import ScheduleContent from "./Content/ScheduleContent";
import {getFormattedDate} from "../../../utils/date";
import NoteService from "../../../services/note";
import ScheduleProvider from "../../../context/ScheduleProvider";
import {NotificationContext} from "../../../context/NotificationProvider";

const Schedule = ({
                      scheduleName,
                      scheduleKey,
                      isLoading,
                      setIsLoading,
                      isAuthCompleted
                  }) => {
    const {showNotification} = useContext(NotificationContext);
    const [isScheduleLoading, setIsScheduleLoading] = useState(true);
    const [isLoadedData, setIsLoadedData] = useState(false);
    const [periods, setPeriods] = useState([]);
    const [currentPeriodValue, setCurrentPeriodValue] = useState("");
    const [schedule, setSchedule] = useState({});
    const [notes, setNotes] = useState([]);

    const fetchSchedule = async () => {
        const service = new ScheduleService();
        let getScheduleFunc = null;
        switch (scheduleName) {
            case "group":
                getScheduleFunc = service.getGroupSchedule.bind(service);
                break;
            case "teacher":
                getScheduleFunc = service.getTeacherSchedule.bind(service);
                break;
            default:
                break;
        }

        if (typeof getScheduleFunc === "function") {
            const {success, data} = await getScheduleFunc(
                currentPeriodValue ? periods[currentPeriodValue].name : {}
            );
            if (success) {
                setSchedule(data);
            } else {
                setSchedule({});
                showNotification(data.detail, {error: true});
            }
        } else {
            throw new Error(`Invalid scheduleName ${scheduleName}`);
        }
    }

    useEffect(() => {
        const loadPeriods = async () => {
            const service = new ScheduleService();
            const {success, data} = await service.getPeriods();
            if (success) {
                setPeriods(
                    data.map((period, index) =>
                        ({name: period, value: index})
                    )
                );
            } else {
                showNotification(data.detail, {error: true});
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
            if (success) {
                setNotes(data.results);
            } else {
                showNotification(data.detail, {error: true});
            }
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