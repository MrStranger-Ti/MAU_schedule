import React, {useContext} from "react";
import {TeacherBookmarksContext} from "../../../../../context/schedule/TeacherBookmarksProvider";
import {ScheduleContext} from "../../../../../context/schedule/ScheduleProvider";
import Button from "../../../../UI/Buttons/Button/Button";
import teacherBookmarksStyles from "../TeacherBookmarks.module.css";
import {ReactComponent as CreateBookmarkIcon} from "../../../../../assets/icons/add-bookmark.svg";

const TeacherBookmarksCreate = () => {
    const {teacherName, teacherKey} = useContext(ScheduleContext);
    const {createTeacherBookmark} = useContext(TeacherBookmarksContext);

    const handleOnClick = () => createTeacherBookmark(teacherName, teacherKey);

    return (
        <Button
            className={teacherBookmarksStyles.button}
            type="button"
            title="Сохранить расписание преподавателя"
            onClick={handleOnClick}
        >
            <CreateBookmarkIcon className={teacherBookmarksStyles.icon}/>
        </Button>
    );
};

export default TeacherBookmarksCreate;