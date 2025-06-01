import React, {useContext} from "react";
import {TeacherBookmarksContext} from "../../../../../context/schedule/TeacherBookmarksProvider";
import {pagesPaths} from "../../../../../AppRoutes";
import {Dropdown} from "react-bootstrap";
import {ReactComponent as DisplayBookmarksIcon} from "../../../../../assets/icons/bookmark-list.svg";
import Button from "../../../../UI/Buttons/Button/Button";
import teacherBookmarksStyles from "../TeacherBookmarks.module.css";
import {ReactComponent as DeleteBookmarkIcon} from "../../../../../assets/icons/delete.svg";
import styles from "./TeacherBookmarksDisplay.module.css"
import RouterDarkLink from "../../../../UI/Links/RouterDarkLink/RouterDarkLink";

const TeacherBookmarksDisplay = () => {
    const {teacherBookmarks, deleteTeacherBookmark} = useContext(TeacherBookmarksContext);

    return (
        <div className={styles.Display}>
            <Dropdown className={styles.Dropdown}>
                <Dropdown.Toggle
                    className={teacherBookmarksStyles.Button}
                    as="button"
                    title="Список закладок преподавателей"
                >
                    <DisplayBookmarksIcon className={teacherBookmarksStyles.Icon}/>
                </Dropdown.Toggle>
                <Dropdown.Menu className={styles.DropdownMenu}>
                    {teacherBookmarks.length > 0
                        ?
                        <React.Fragment>
                            {teacherBookmarks.map(bookmark =>
                                <Dropdown.Item
                                    className={styles.DropdownItem}
                                    as="div"
                                    key={bookmark["id"]}
                                >
                                    <RouterDarkLink
                                        className={styles.Link}
                                        to={pagesPaths.schedule.getTeacherURL(bookmark["teacher_key"], bookmark["teacher_name"])}
                                    >
                                        {bookmark["teacher_name"]}
                                    </RouterDarkLink>
                                    <Button
                                        className={`${teacherBookmarksStyles.Button} ${styles.DeleteButton}`}
                                        type="button"
                                        title="Удалить расписание преподавателя"
                                        onClick={() => deleteTeacherBookmark(bookmark)}
                                    >
                                        <DeleteBookmarkIcon className={styles.DeleteIcon}/>
                                    </Button>
                                </Dropdown.Item>
                            )}
                        </React.Fragment>
                        :
                        <Dropdown.Item className={styles.DropdownItem} as="div">
                            <p className={styles.EmptyDescr}>Здесь будут отображаться сохраненные расписания</p>
                        </Dropdown.Item>
                    }
                </Dropdown.Menu>
            </Dropdown>
        </div>
    );
};

export default TeacherBookmarksDisplay;