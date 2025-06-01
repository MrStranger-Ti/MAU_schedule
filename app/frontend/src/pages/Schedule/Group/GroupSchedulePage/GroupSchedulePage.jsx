import React, {useState} from "react";
import BaseSchedule from "../../BaseSchedule";
import {useAuth} from "../../../../hooks/auth/useAuth";
import {LoadingContext} from "../../../../context/main/LoadingProvider";
import {GroupScheduleProvider} from "../../../../context/schedule/ScheduleProvider";
import GroupScheduleContent from "../GroupScheduleContent/GroupScheduleContent";

const GroupSchedulePage = () => {
    const [isLoading, setIsLoading] = useState(true);

    useAuth(setIsLoading, {
        stopLoading: false,
        protect: true
    });

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseSchedule>
                <GroupScheduleProvider>
                    <GroupScheduleContent/>
                </GroupScheduleProvider>
            </BaseSchedule>
        </LoadingContext.Provider>
    );
};

export default GroupSchedulePage;