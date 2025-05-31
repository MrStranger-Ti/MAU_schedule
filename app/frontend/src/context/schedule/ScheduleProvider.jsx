import React, {createContext, useContext, useState} from "react";
import {NotificationContext} from "../main/NotificationProvider";
import ScheduleService from "../../services/schedule";
import NotesProvider from "./NotesProvider";
import PeriodsProvider from "./PeriodsProvider";
import {AuthContext} from "../main/AuthProvider";
import {useParams} from "react-router-dom";
import TeacherBookmarksProvider from "./TeacherBookmarksProvider";

export const ScheduleContext = createContext(null);

const GroupScheduleProvider = ({children}) => {
    const {userData} = useContext(AuthContext);
    const {showNotification} = useContext(NotificationContext);
    const [schedule, setSchedule] = useState({});
    const [isScheduleLoading, setIsScheduleLoading] = useState(false);
    const [isScheduleLoaded, setIsScheduleLoaded] = useState(false);

    const fetchSchedule = async (period) => {
        const service = new ScheduleService();
        const {success, data} = await service.getGroupSchedule(period);
        if (success) {
            setSchedule(data);
        } else {
            setSchedule({});
            showNotification(data.detail, {error: true});
        }

        setIsScheduleLoaded(true);
    }

    return (
        <ScheduleContext.Provider value={{
            scheduleName: "group", scheduleKey: userData.group,
            fetchSchedule, isScheduleLoaded,
            schedule, setSchedule,
            isScheduleLoading, setIsScheduleLoading
        }}>
            <PeriodsProvider>
                <NotesProvider>
                    {children}
                </NotesProvider>
            </PeriodsProvider>
        </ScheduleContext.Provider>
    );
};

const TeacherScheduleProvider = ({children}) => {
    const {keyName} = useParams();
    const {showNotification} = useContext(NotificationContext);
    const [schedule, setSchedule] = useState({});
    const [isScheduleLoading, setIsScheduleLoading] = useState(false);

    const decodeKeyName = () => {
        const [teacherKey, teacherName] = decodeURIComponent(keyName).split("~");
        return {teacherKey, teacherName};
    }

    const fetchSchedule = async (period) => {
        const service = new ScheduleService();
        const {success, data} = await service.getTeacherSchedule(
            period,
            decodeKeyName().teacherKey
        );
        if (success) {
            setSchedule(data);
        } else {
            setSchedule({});
            showNotification(data.detail, {error: true});
        }
    }

    return (
        <ScheduleContext.Provider value={{
            ...decodeKeyName(),
            scheduleKey: decodeKeyName().teacherKey,
            fetchSchedule,
            schedule,
            setSchedule,
            isScheduleLoading,
            setIsScheduleLoading
        }}>
            <PeriodsProvider>
                <NotesProvider>
                    <TeacherBookmarksProvider>
                        {children}
                    </TeacherBookmarksProvider>
                </NotesProvider>
            </PeriodsProvider>
        </ScheduleContext.Provider>
    );
};

export {GroupScheduleProvider, TeacherScheduleProvider};