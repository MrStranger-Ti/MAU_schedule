import React, {useContext, useEffect, useState} from "react";
import SunEditor from "suneditor-react";
import {EditorContext} from "../../../../../context/schedule/EditorProvider";
import DisplayBtns from "../ButtonsBlock/DisplayBtns/DisplayBtns";
import CreateBtns from "../ButtonsBlock/CreateBtns/CreateBtns";
import UpdateBtns from "../ButtonsBlock/UpdateBtns/UpdateBtns";
import Form from "../../../../UI/Form/Form";
import styles from "./NoteEditor.module.css";

const NoteEditor = () => {
    const {
        editorModes, editorOptions,
        editorMode,
        editorText, setEditorText,
        getSunEditorInstance,
        createEditorNote, updateEditorNote, deleteEditorNote
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

    const getAction = () => {
        const editorActions = {
            [editorModes.display]: deleteEditorNote,
            [editorModes.create]: createEditorNote,
            [editorModes.update]: updateEditorNote
        }
        return editorActions[editorMode] || null;
    }

    const onSubmit = async (e) => {
        e.preventDefault();

        const action = getAction();
        if (typeof action === "function") {
            setIsBtnLoading(true);

            await action();

            setIsBtnLoading(false);
        }
    }

    return (
        <Form className={styles.form} onSubmit={onSubmit}>
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