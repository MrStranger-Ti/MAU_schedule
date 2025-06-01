import React, {useContext, useEffect} from "react";
import {AuthContext} from "../../../../context/main/AuthProvider";
import {LoadingContext} from "../../../../context/main/LoadingProvider";
import {useSchedule} from "../../../../hooks/schedule/useSchedule";
import Spinner from "../../../../components/Spinner/Spinner";
import Schedule from "../../../../components/Schedule/Schedule";
import GroupTitleBlock from "../GroupTitleBlock/GroupTitleBlock";
import {useLocation} from "react-router-dom";
import {useChangeLocation} from "../../../../hooks/general/useChangeLocation";

const GroupScheduleContent = () => {
    const {isAuthCompleted} = useContext(AuthContext);
    const {isLoading, setIsLoading} = useContext(LoadingContext);

    const {isScheduleDataLoaded} = useSchedule([isAuthCompleted, isLoading]);

    useEffect(() => {
        if (isScheduleDataLoaded) setIsLoading(false);
    }, [isScheduleDataLoaded]);

    useChangeLocation(() => setIsLoading(true));

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