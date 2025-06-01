import React, {createContext, useContext, useState} from "react";
import NoteService from "../../services/note";
import {NotificationContext} from "../main/NotificationProvider";
import {AuthContext} from "../main/AuthProvider";
import {ScheduleContext} from "./ScheduleProvider";

export const NotesContext = createContext(null);

const NotesProvider = ({children}) => {
    const {userData} = useContext(AuthContext);
    const {scheduleName, scheduleKey} = useContext(ScheduleContext);
    const {showNotification} = useContext(NotificationContext);
    const [notes, setNotes] = useState([]);
    const [isNotesLoaded, setIsNotesLoaded] = useState(false);

    const fetchNotes = async () => {
        const service = new NoteService();
        const {success, data} = await service.getAll();
        if (success) {
            setNotes(data.results);
        } else {
            showNotification(data.detail, {error: true});
        }

        setIsNotesLoaded(true);
    }

    const createNote = async ({day, lessonNumber, text}) => {
        const service = new NoteService();
        const {success, data} = await service.create({
            schedule_name: scheduleName,
            schedule_key: scheduleKey,
            day: day,
            lesson_number: lessonNumber,
            text: text,
            user: userData.id
        })

        if (success) {
            setNotes([...notes, data]);
        }
        return {success, data};
    }

    const updateNote = async ({id, text}) => {
        const service = new NoteService();
        const {success, data} = await service.update(id, text)
        if (success) {
            setNotes([...notes].map(note => {
                if (note.id === id) {
                    return {...note, text};
                }
                return note;
            }));
        }

        return {success, data};
    }

    const deleteNote = async ({id}) => {
        const service = new NoteService();
        const {success, data} = await service.delete(id)
        if (success) {
            setNotes(notes.filter((note) => note.id !== id));
        }

        return {success, data};
    }

    return (
        <NotesContext.Provider value={{
            fetchNotes, isNotesLoaded, setIsNotesLoaded,
            notes, setNotes,
            createNote, updateNote, deleteNote
        }}>
            {children}
        </NotesContext.Provider>
    );
};

export default NotesProvider;