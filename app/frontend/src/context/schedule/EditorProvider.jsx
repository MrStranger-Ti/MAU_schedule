import React, {createContext, useContext, useEffect, useRef, useState} from "react";
import {ScheduleRowContext} from "./ScheduleRowProvider";
import NoteService from "../../services/note";
import {AuthContext} from "../main/AuthProvider";
import {ScheduleContext} from "./ScheduleProvider";
import {NotesContext} from "./NotesProvider";
import {NotificationContext} from "../main/NotificationProvider";

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
    const {createNote, updateNote, deleteNote} = useContext(NotesContext);
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

    const createEditorNote = async () => {
        if (editorRef.current.getText() === "") return;

        const {success, data} = await createNote({
            day,
            lessonNumber,
            text: editorRef.current.getContents()
        });

        if (success) {
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

    const updateEditorNote = async () => {
        if (editorRef.current.getContents() === rowNote.text) {
            setEditorMode(editorModes.display);
            return;
        }

        const {success, data} = await updateNote({
            id: rowNote.id,
            text: editorRef.current.getContents()
        });
        if (success) {
            setRowNote(data);
            setEditorText(data.text);
            setEditorMode(editorModes.display);
            showNotification("Заметка успешно обновлена!");
        } else {
            showNotification("Не удалось обновить заметку", {error: true});
        }
    }

    const deleteEditorNote = async () => {
        const {success} = await deleteNote({id: rowNote.id});
        if (success) {
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
            createEditorNote, updateEditorNote, deleteEditorNote
        }}>
            {children}
        </EditorContext.Provider>
    );
};

export default EditorProvider;