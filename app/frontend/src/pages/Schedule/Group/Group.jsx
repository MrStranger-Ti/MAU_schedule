import React, {useContext, useState} from "react";
import BaseSchedule from "../BaseSchedule";
import {useAuth} from "../../../hooks/useAuth";
import {LoadingContext} from "../../../context/main/LoadingProvider";
import ScheduleProvider from "../../../context/schedule/ScheduleProvider";
import {AuthContext} from "../../../context/main/AuthProvider";
import Schedule from "../../../components/Schedule/Schedule";

const Group = () => {
    const {userData} = useContext(AuthContext);
    const [isLoading, setIsLoading] = useState(true);

    useAuth(setIsLoading, {
        stopLoading: false,
        protect: true
    });

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseSchedule>
                <ScheduleProvider scheduleName="group" scheduleKey={userData.group}>
                    <Schedule/>
                </ScheduleProvider>
            </BaseSchedule>
        </LoadingContext.Provider>
    );
};

export default Group;