import React, {useState} from "react";
import {LoadingContext} from "../../../../context/main/LoadingProvider";
import BaseSchedule from "../../BaseSchedule";
import {useAuth} from "../../../../hooks/auth/useAuth";
import {TeacherScheduleProvider} from "../../../../context/schedule/ScheduleProvider";
import TeacherScheduleContent from "../TecherScheduleContent/TeacherScheduleContent";

const TeacherSchedulePage = () => {
    const [isLoading, setIsLoading] = useState(true);

    useAuth(setIsLoading, {
        stopLoading: false,
        protect: true
    });

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseSchedule>
                <TeacherScheduleProvider>
                    <TeacherScheduleContent/>
                </TeacherScheduleProvider>
            </BaseSchedule>
        </LoadingContext.Provider>
    );
};

export default TeacherSchedulePage;