import React, {useContext, useEffect, useRef, useState} from "react";
import Form from "../../../../../components/UI/Form/Form";
import SunEditor from "suneditor-react";
import DisplayBtns from "./Buttons/DisplayBtns";
import CreateBtns from "./Buttons/CreateBtns";
import UpdateBtns from "./Buttons/UpdateBtns";
import {EditorContext} from "../../../../../context/EditorProvider";
import NoteService from "../../../../../services/note";
import {ScheduleContext} from "../../../../../context/ScheduleProvider";
import {ScheduleRowContext} from "../../../../../context/ScheduleRowProvider";
import {AuthContext} from "../../../../../context/AuthProvider";
import {NotificationContext} from "../../../../../context/NotificationProvider";

export const editorModes = {
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

const NoteEditor = () => {
    const {userData} = useContext(AuthContext);
    const {scheduleName, scheduleKey, notes, setNotes} = useContext(ScheduleContext);
    const {day, lessonNumber, rowNote, setRowNote} = useContext(ScheduleRowContext);
    const {editorMode, setEditorMode} = useContext(EditorContext);
    const {showNotification} = useContext(NotificationContext);
    const [ButtonsComponent, setButtonsComponent] = useState(null);
    const [isBtnLoading, setIsBtnLoading] = useState(false);

    const editorRef = useRef(null);

    const getSunEditorInstance = (sunEditor) => {
        editorRef.current = sunEditor;
    }

    const ButtonsGroups = {
        display: <DisplayBtns isBtnLoading={isBtnLoading}/>,
        create: <CreateBtns isBtnLoading={isBtnLoading}/>,
        update: <UpdateBtns isBtnLoading={isBtnLoading}/>
    };

    useEffect(() => {
        setButtonsComponent(ButtonsGroups[editorMode]);
    }, [editorMode, isBtnLoading]);

    const createNote = async () => {
        const editorText = editorRef.current.getText();
        if (editorText === "") return;

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
            setEditorMode(editorModes.display);
            showNotification("Заметка успешно создана!");
        } else {
            showNotification(data, {error: true});
        }
    }

    const updateNote = async () => {
        const editorContent = editorRef.current.getContents();
        if (editorContent === rowNote.text) {
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
            setEditorMode(editorModes.display);
            showNotification("Заметка успешно обновлена!");
        } else {
            showNotification(data, {error: true});
        }
    }

    const deleteNote = async () => {
        const service = new NoteService();
        const {success, data} = await service.delete(rowNote.id)
        if (success) {
            setNotes(notes.filter((iterNote) => iterNote.id !== rowNote.id));
            setRowNote(null);
            setEditorMode(editorModes.create);
            showNotification("Заметка успешно удалена!");
        } else {
            showNotification(data, {error: true});
        }
    }

    let onSubmitFunc = null;
    if (editorMode === editorModes.display) {
        onSubmitFunc = () => deleteNote();
    } else if (editorMode === editorModes.create) {
        onSubmitFunc = () => createNote();
    } else {
        onSubmitFunc = () => updateNote();
    }

    const onSubmit = async (e) => {
        e.preventDefault();

        if (typeof onSubmitFunc === "function") {
            setIsBtnLoading(true);

            await onSubmitFunc();

            setIsBtnLoading(false);
        }
    }

    return (
        <Form className="note-block__form flex" onSubmit={onSubmit}>
            <SunEditor
                getSunEditorInstance={getSunEditorInstance}
                lang="ru"
                setOptions={editorOptions}
                setContents={rowNote ? rowNote.text : ""}
                disable={isBtnLoading || editorMode === editorModes.display}
                hideToolbar={editorMode === editorModes.display}
            />
            {ButtonsComponent}
        </Form>
    );
};

export default NoteEditor;