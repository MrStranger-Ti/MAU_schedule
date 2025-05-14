import React, {useContext, useState} from "react";
import BaseSchedule from "../BaseSchedule";
import Schedule from "../Base/Schedule";
import {useAuth} from "../../../hooks/useAuth";
import {LoadingContext} from "../../../context/LoadingProvider";
import {AuthContext} from "../../../context/AuthProvider";

const Group = () => {
    const {userData} = useContext(AuthContext);
    const [isLoading, setIsLoading] = useState(true);
    const {isAuthCompleted} = useAuth(setIsLoading, {
        stopLoading: false,
        protect: true
    });

    return (
        <LoadingContext value={{isLoading, setIsLoading}}>
            <BaseSchedule>
                <Schedule
                    scheduleName="group"
                    scheduleKey={userData.group}
                    isLoading={isLoading}
                    setIsLoading={setIsLoading}
                    isAuthCompleted={isAuthCompleted}
                />
            </BaseSchedule>
        </LoadingContext>
    );
};

export default Group;