import React, {createContext, useContext, useEffect, useState} from "react";
import {NotificationContext} from "../main/NotificationProvider";
import ScheduleService from "../../services/schedule";
import NotesProvider from "./NotesProvider";
import PeriodsProvider from "./PeriodsProvider";

export const ScheduleContext = createContext(null);

const scheduleNames = ["group", "teacher"]

const ScheduleProvider = ({children, scheduleName, scheduleKey}) => {
    const {showNotification} = useContext(NotificationContext);
    const [schedule, setSchedule] = useState({});
    const [isScheduleLoading, setIsScheduleLoading] = useState(false);

    useEffect(() => {
        if (!scheduleNames.includes(scheduleName)) scheduleName = "group";
    }, []);

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
                throw new Error(`Invalid scheduleName: ${scheduleName}`);
        }

        const {success, data} = await getScheduleFunc(period);
        if (success) {
            setSchedule(data);
        } else {
            setSchedule({});
            showNotification(data.detail, {error: true});
        }
    }

    return (
        <ScheduleContext.Provider value={{
            scheduleName,
            scheduleKey,
            fetchSchedule,
            schedule,
            setSchedule,
            isScheduleLoading,
            setIsScheduleLoading
        }}>
            <PeriodsProvider>
                <NotesProvider>
                    {children}
                </NotesProvider>
            </PeriodsProvider>
        </ScheduleContext.Provider>
    );
};

export default ScheduleProvider;