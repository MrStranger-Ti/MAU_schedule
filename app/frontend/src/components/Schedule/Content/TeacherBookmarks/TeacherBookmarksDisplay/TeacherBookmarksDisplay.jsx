import React, {useContext} from "react";
import {TeacherBookmarksContext} from "../../../../../context/schedule/TeacherBookmarksProvider";
import {pagesPaths} from "../../../../../AppRoutes";
import {Dropdown} from "react-bootstrap";
import {ReactComponent as DisplayBookmarksIcon} from "../../../../../assets/icons/bookmark-list.svg";
import Button from "../../../../UI/Buttons/Button/Button";
import teacherBookmarksStyles from "../TeacherBookmarks.module.css";
import {ReactComponent as DeleteBookmarkIcon} from "../../../../../assets/icons/delete2.svg";
import RouterDarkLink from "../../../../UI/Links/RouterDarkLink/RouterDarkLink";
import styles from "./TeacherBookmarksDisplay.module.css"

const TeacherBookmarksDisplay = () => {
    const {teacherBookmarks, deleteTeacherBookmark} = useContext(TeacherBookmarksContext);

    return (
        <div className={styles.display}>
            <Dropdown className={styles.dropdown}>
                <Dropdown.Toggle
                    className={teacherBookmarksStyles.button}
                    as="button"
                    title="Список закладок преподавателей"
                >
                    <DisplayBookmarksIcon className={teacherBookmarksStyles.icon}/>
                </Dropdown.Toggle>
                <Dropdown.Menu className={styles.dropdownMenu}>
                    {teacherBookmarks.length > 0
                        ?
                        <React.Fragment>
                            {teacherBookmarks.map(bookmark =>
                                <Dropdown.Item
                                    className={styles.dropdownItem}
                                    as="div"
                                    key={bookmark["id"]}
                                >
                                    <RouterDarkLink
                                        className={styles.link}
                                        to={pagesPaths.schedule.getTeacherURL(bookmark["teacher_key"], bookmark["teacher_name"])}
                                    >
                                        {bookmark["teacher_name"]}
                                    </RouterDarkLink>
                                    <Button
                                        className={`${teacherBookmarksStyles.button} ${styles.deleteButton}`}
                                        type="button"
                                        title="Удалить расписание преподавателя"
                                        onClick={() => deleteTeacherBookmark(bookmark)}
                                    >
                                        <DeleteBookmarkIcon className={styles.deleteIcon}/>
                                    </Button>
                                </Dropdown.Item>
                            )}
                        </React.Fragment>
                        :
                        <Dropdown.Item className={styles.dropdownItem} as="div">
                            <p className={styles.emptyDescr}>Здесь будут отображаться сохраненные расписания</p>
                        </Dropdown.Item>
                    }
                </Dropdown.Menu>
            </Dropdown>
        </div>
    );
};

export default TeacherBookmarksDisplay;