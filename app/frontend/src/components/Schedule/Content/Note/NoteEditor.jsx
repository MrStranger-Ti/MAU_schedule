import React, {useContext, useEffect, useState} from "react";
import SunEditor from "suneditor-react";
import {EditorContext} from "../../../../context/schedule/EditorProvider";
import DisplayBtns from "./Buttons/DisplayBtns";
import CreateBtns from "./Buttons/CreateBtns";
import UpdateBtns from "./Buttons/UpdateBtns";
import Form from "../../../UI/Form/Form";

const NoteEditor = () => {
    const {
        editorModes, editorOptions,
        editorMode,
        editorText, setEditorText,
        getSunEditorInstance,
        createNote, updateNote, deleteNote
    } = useContext(EditorContext);
    const [ButtonsComponent, setButtonsComponent] = useState(null);
    const [isBtnLoading, setIsBtnLoading] = useState(false);

    const ButtonsGroups = {
        display: <DisplayBtns isBtnLoading={isBtnLoading}/>,
        create: <CreateBtns isBtnLoading={isBtnLoading}/>,
        update: <UpdateBtns isBtnLoading={isBtnLoading}/>
    };

    useEffect(() => {
        setButtonsComponent(ButtonsGroups[editorMode]);
    }, [editorMode, isBtnLoading]);

    let onSubmitFunc = null;
    if (editorMode === editorModes.display) {
        onSubmitFunc = deleteNote;
    } else if (editorMode === editorModes.create) {
        onSubmitFunc = createNote;
    } else {
        onSubmitFunc = updateNote;
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
                setContents={editorText}
                disable={isBtnLoading || editorMode === editorModes.display}
                hideToolbar={editorMode === editorModes.display}
                onChange={(content) => setEditorText(content)}
            />
            {ButtonsComponent}
        </Form>
    );
};

export default NoteEditor;