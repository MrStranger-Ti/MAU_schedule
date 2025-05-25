import React, {createContext, useContext, useState} from "react";
import {NotificationContext} from "../NotificationProvider";
import ScheduleService from "../../services/schedule";
import NotesProvider from "./NotesProvider";
import PeriodsProvider from "./PeriodsProvider";

export const ScheduleContext = createContext(null);

const ScheduleProvider = ({children, scheduleName, scheduleKey}) => {
    const {showNotification} = useContext(NotificationContext);
    const [schedule, setSchedule] = useState({});
    const [isScheduleLoading, setIsScheduleLoading] = useState(false);

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