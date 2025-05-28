import React, {useState} from "react";
import {LoadingContext} from "../../../context/main/LoadingProvider";
import BaseSchedule from "../BaseSchedule";
import ScheduleProvider from "../../../context/schedule/ScheduleProvider";
import {useAuth} from "../../../hooks/useAuth";
import TeacherBookmarksProvider from "../../../context/schedule/TeacherBookmarksProvider";
import Schedule from "../../../components/Schedule/Schedule";
import {useParams} from "react-router-dom";

const Teacher = () => {
    const {teacherKey} = useParams();

    const [isLoading, setIsLoading] = useState(false);

    useAuth(setIsLoading, {
        protect: true
    })

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseSchedule>
                <ScheduleProvider scheduleName="teacher" scheduleKey={teacherKey}>
                    <TeacherBookmarksProvider>
                        <Schedule/>
                    </TeacherBookmarksProvider>
                </ScheduleProvider>
            </BaseSchedule>
        </LoadingContext.Provider>
);
};

export default Teacher;