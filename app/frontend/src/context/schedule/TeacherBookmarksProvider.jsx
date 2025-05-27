import React, {createContext, useContext, useState} from "react";
import TeacherBookmarksService from "../../services/teacherBookmarks";
import {NotificationContext} from "../main/NotificationProvider";

export const TeacherBookmarksContext = createContext(null);

const TeacherBookmarksProvider = ({children}) => {
    const {showNotification} = useContext(NotificationContext);
    const [teacherBookmarks, setTeacherBookmarks] = useState([]);

    const fetchTeacherBookmarks = async () => {
        const service = new TeacherBookmarksService();
        const {success, data} = await service.getAll();
        if (success) {
            setTeacherBookmarks(data.results);
        } else {
            setTeacherBookmarks([]);
            showNotification(data.detail, {error: true});
        }
    }

    const deleteTeacherBookmark = async (bookmark) => {
        const service = new TeacherBookmarksService();
        const {success} = await service.delete(bookmark.id);
        if (success) {
            setTeacherBookmarks(
                [...teacherBookmarks].filter(
                    bookmarkItem => bookmarkItem.id !== bookmark.id
                )
            );
            showNotification(`Закладка ${bookmark.teacher_name} успешно удалена`);
        } else {
            showNotification(`Не удалось удалить закладку ${bookmark.teacher_name}`);
        }
    }

    return (
        <TeacherBookmarksContext.Provider value={{
            teacherBookmarks, setTeacherBookmarks,
            fetchTeacherBookmarks,
            deleteTeacherBookmark
        }}>
            {children}
        </TeacherBookmarksContext.Provider>
    );
};

export default TeacherBookmarksProvider;