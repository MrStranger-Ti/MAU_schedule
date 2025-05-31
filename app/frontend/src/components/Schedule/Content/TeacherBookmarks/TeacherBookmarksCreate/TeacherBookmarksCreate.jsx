import React, {useContext} from "react";
import {TeacherBookmarksContext} from "../../../../../context/schedule/TeacherBookmarksProvider";
import {ScheduleContext} from "../../../../../context/schedule/ScheduleProvider";
import Button from "../../../../UI/Buttons/Button/Button";
import styles from "../TeacherBookmarks.module.css";
import {ReactComponent as CreateBookmarkIcon} from "../../../../../assets/icons/add-bookmark.svg"

const TeacherBookmarksCreate = () => {
    const {teacherName, teacherKey} = useContext(ScheduleContext);
    const {createTeacherBookmark} = useContext(TeacherBookmarksContext);

    const handleOnClick = () => createTeacherBookmark(teacherName, teacherKey);

    return (
        <Button
            className={styles.Button}
            type="button"
            onClick={handleOnClick}
        >
            <CreateBookmarkIcon className={styles.BookmarkIcon}/>
        </Button>
    );
};

export default TeacherBookmarksCreate;