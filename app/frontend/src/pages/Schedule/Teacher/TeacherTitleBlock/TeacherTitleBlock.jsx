import React, {useContext, useEffect, useState} from 'react';
import PeriodForm from "../../../../components/Schedule/Content/PeriodForm/PeriodForm";
import TeacherBookmarksDisplay from "../../../../components/Schedule/Content/TeacherBookmarks/TeacherBookmarksDisplay/TeacherBookmarksDisplay";
import TeacherBookmarksCreate from "../../../../components/Schedule/Content/TeacherBookmarks/TeacherBookmarksCreate/TeacherBookmarksCreate";
import {ScheduleContext} from "../../../../context/schedule/ScheduleProvider";
import {TeacherBookmarksContext} from "../../../../context/schedule/TeacherBookmarksProvider";

const TeacherTitleBlock = () => {
    const {teacherName, teacherKey} = useContext(ScheduleContext);
    const {teacherBookmarks, existsTeacherBookmark} = useContext(TeacherBookmarksContext);
    const [showBookmarkCreate, setShowBookmarkCreate] = useState(false);

    useEffect(() => {
        setShowBookmarkCreate(!existsTeacherBookmark(teacherKey));
    }, [teacherBookmarks]);

    return (
        <div className="schedule__title-block flex">
            <div className="schedule__title-left-block flex">
                <h1 className="schedule__title title">{teacherName}</h1>
                <TeacherBookmarksDisplay/>
                {showBookmarkCreate && <TeacherBookmarksCreate/>}
            </div>
            <PeriodForm/>
        </div>
    );
};

export default TeacherTitleBlock;