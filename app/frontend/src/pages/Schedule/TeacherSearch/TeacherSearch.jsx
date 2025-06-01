import React, {useState} from 'react';
import {LoadingContext} from "../../../context/main/LoadingProvider";
import BaseSchedule from "../BaseSchedule";
import {useAuth} from "../../../hooks/auth/useAuth";
import TeacherBookmarksProvider from "../../../context/schedule/TeacherBookmarksProvider";
import TeacherSearchContent from "./TeacherSearchContent";

const TeacherSearch = () => {
    const [isLoading, setIsLoading] = useState(true);

    useAuth(setIsLoading, {
        stopLoading: false,
        protect: true
    });


    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <BaseSchedule>
                <TeacherBookmarksProvider>
                    <TeacherSearchContent/>
                </TeacherBookmarksProvider>
            </BaseSchedule>
        </LoadingContext.Provider>
    );
};

export default TeacherSearch;