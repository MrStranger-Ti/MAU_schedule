import React, {createContext, useContext, useState} from "react";
import NoteService from "../../services/note";
import {NotificationContext} from "../NotificationProvider";

export const NotesContext = createContext(null);

const NotesProvider = ({children}) => {
    const {showNotification} = useContext(NotificationContext);
    const [notes, setNotes] = useState([]);
    
    const fetchNotes = async () => {
        const service = new NoteService();
        const {success, data} = await service.getAll();
        if (success) {
            setNotes(data.results);
        } else {
            showNotification(data.detail, {error: true});
        }
    }
    
    return (
        <NotesContext.Provider value={{fetchNotes, notes, setNotes}}>
            {children}
        </NotesContext.Provider>
    );
};

export default NotesProvider;