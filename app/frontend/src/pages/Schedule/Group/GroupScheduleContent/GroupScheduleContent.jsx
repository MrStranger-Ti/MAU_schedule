import React, {useContext, useEffect} from "react";
import {AuthContext} from "../../../../context/main/AuthProvider";
import {LoadingContext} from "../../../../context/main/LoadingProvider";
import {useSchedule} from "../../../../hooks/useSchedule";
import Spinner from "../../../../components/Spinner/Spinner";
import Schedule from "../../../../components/Schedule/Schedule";
import GroupTitleBlock from "../GroupTitleBlock/GroupTitleBlock";

const GroupScheduleContent = () => {
    const {isAuthCompleted} = useContext(AuthContext);
    const {isLoading, setIsLoading} = useContext(LoadingContext);

    const {isScheduleDataLoaded} = useSchedule(isAuthCompleted);

    useEffect(() => {
        if (isScheduleDataLoaded) setIsLoading(false);
    }, [isScheduleDataLoaded]);

    return (
        <React.Fragment>
            {isLoading
                ?
                <Spinner/>
                :
                <div className="schedule__content">
                    <GroupTitleBlock/>
                    <Schedule/>
                </div>
            }
        </React.Fragment>
    );
};

export default GroupScheduleContent;