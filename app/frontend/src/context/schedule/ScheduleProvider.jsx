import React, {createContext, useContext, useState} from "react";
import {NotificationContext} from "./NotificationProvider";
import ScheduleService from "../services/schedule";
import NoteService from "../services/note";

export const ScheduleContext = createContext(null);

const ScheduleProvider = ({children, scheduleName, scheduleKey}) => {
    const [isScheduleLoading, setIsScheduleLoading] = useState(false);
    const {showNotification} = useContext(NotificationContext);
    const [periods, setPeriods] = useState([]);
    const [schedule, setSchedule] = useState({});
    const [notes, setNotes] = useState([]);

    const fetchSchedule = async (period) => {
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
            const {success, data} = await getScheduleFunc(period);
            if (success) {
                setSchedule(data);
            } else {
                setSchedule({});
                showNotification(data.detail, {error: true});
            }
        } else {
            throw new Error(`Invalid scheduleName: ${scheduleName}`);
        }
    }

    const fetchNotes = async () => {
        const service = new NoteService();
        const {success, data} = await service.getAll();
        if (success) {
            setNotes(data.results);
        } else {
            showNotification(data.detail, {error: true});
        }
    }

    const fetchPeriods = async () => {
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

    return (
        <ScheduleContext.Provider value={{
            scheduleName,
            scheduleKey,
            fetchPeriods,
            fetchSchedule,
            fetchNotes,
            periods,
            setPeriods,
            schedule,
            setSchedule,
            notes,
            setNotes,
            isScheduleLoading,
            setIsScheduleLoading
        }}>
            {children}
        </ScheduleContext.Provider>
    );
};

export default ScheduleProvider;