import React, {useContext, useEffect} from 'react';
import {LoadingContext} from "../../../../context/main/LoadingProvider";
import {useSchedule} from "../../../../hooks/schedule/useSchedule";
import {AuthContext} from "../../../../context/main/AuthProvider";
import Spinner from "../../../../components/Spinner/Spinner";
import Schedule from "../../../../components/Schedule/Schedule";
import TeacherTitleBlock from "../TeacherTitleBlock/TeacherTitleBlock";
import {TeacherBookmarksContext} from "../../../../context/schedule/TeacherBookmarksProvider";
import {useChangeLocation} from "../../../../hooks/general/useChangeLocation";

const TeacherScheduleContent = () => {
    const {isAuthCompleted} = useContext(AuthContext);
    const {isLoading, setIsLoading} = useContext(LoadingContext);
    const {fetchTeacherBookmarks} = useContext(TeacherBookmarksContext);

    const {isScheduleDataLoaded} = useSchedule([isAuthCompleted, isLoading]);

    useEffect(() => {
        const loadBookmarks = async () => {
            await fetchTeacherBookmarks();
            setIsLoading(false);
        }

        if (isScheduleDataLoaded) loadBookmarks();
    }, [isScheduleDataLoaded]);

    useChangeLocation(() => setIsLoading(true));

    return (
        <React.Fragment>
            {isLoading
                ?
                <Spinner/>
                :
                <div className="schedule__content">
                    <TeacherTitleBlock/>
                    <Schedule/>
                </div>
            }
        </React.Fragment>
    );
};

export default TeacherScheduleContent;