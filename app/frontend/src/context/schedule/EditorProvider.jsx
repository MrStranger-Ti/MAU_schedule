import React, {createContext, useContext, useEffect, useRef, useState} from "react";
import {ScheduleRowContext} from "./ScheduleRowProvider";
import NoteService from "../../services/note";
import {AuthContext} from "../AuthProvider";
import {ScheduleContext} from "./ScheduleProvider";
import {NotesContext} from "./NotesProvider";
import {NotificationContext} from "../NotificationProvider";

export const EditorContext = createContext(null);

const editorModes = {
    display: "display",
    create: "create",
    update: "update"
};

const editorOptions = {
    width: "100%",
    height: "100%",
    maxHeight: "1000px",
    resizingBar: false,
    minHeight: "200px",
    font: ["Montserrat"],
    className: "note-block__editable",
    buttonList: [
        ["undo", "redo"],
        [":p-More Paragraph-default.more_paragraph", "bold", "underline", "italic", "strike"],
        ["textStyle"],
        ["align", "list"],
        ["fullScreen"]
    ]
};

export const EditorProvider = ({children}) => {
    const {userData} = useContext(AuthContext);
    const {scheduleName, scheduleKey} = useContext(ScheduleContext);
    const {notes, setNotes} = useContext(NotesContext);
    const {
        day,
        lessonNumber,
        rowNote,
        setRowNote
    } = useContext(ScheduleRowContext);
    const {showNotification} = useContext(NotificationContext);
    const [editorMode, setEditorMode] = useState(
        rowNote ? editorModes.display : editorModes.create
    );
    const [editorText, setEditorText] = useState(rowNote ? rowNote.text : "");

    const editorRef = useRef(null);

    const getSunEditorInstance = (sunEditor) => {
        editorRef.current = sunEditor;
    }

    const createNote = async () => {
        if (editorRef.current.getText() === "") return;

        const service = new NoteService();
        const {success, data} = await service.create({
            schedule_name: scheduleName,
            schedule_key: scheduleKey,
            day: day,
            lesson_number: lessonNumber,
            text: editorRef.current.getContents(),
            user: userData.id
        })

        if (success) {
            setNotes([...notes, data]);
            setRowNote(data);
            setEditorText(data.text);
            setEditorMode(editorModes.display);
            showNotification("Заметка успешно создана!");
        } else {
            showNotification(
                "Заметку можно создать только на текущую неделю и на следующие две",
                {error: true}
            );
        }
    }

    const updateNote = async () => {
        if (editorRef.current.getContents() === rowNote.text) {
            setEditorMode(editorModes.display);
            return;
        }

        const service = new NoteService();
        const {success, data} = await service.update(rowNote.id, {
            text: editorRef.current.getContents(),
        })
        if (success) {
            setNotes([...notes, data]);
            setRowNote(data);
            setEditorText(data.text);
            setEditorMode(editorModes.display);
            showNotification("Заметка успешно обновлена!");
        } else {
            showNotification("Не удалось обновить заметку", {error: true});
        }
    }

    const deleteNote = async () => {
        const service = new NoteService();
        const {success} = await service.delete(rowNote.id)
        if (success) {
            setNotes(notes.filter((iterNote) => iterNote.id !== rowNote.id));
            setRowNote(null);
            setEditorText("");
            setEditorMode(editorModes.create);
            showNotification("Заметка успешно удалена!");
        } else {
            showNotification("Не удалось удалить заметку", {error: true});
        }
    }

    return (
        <EditorContext.Provider value={{
            editorModes, editorOptions, editorRef,
            editorMode, setEditorMode,
            editorText, setEditorText,
            getSunEditorInstance,
            createNote, updateNote, deleteNote
        }}>
            {children}
        </EditorContext.Provider>
    );
};

export default EditorProvider;