import React, {useContext, useState} from "react";
import {Collapse} from "react-bootstrap";
import NoteEditor, {editorModes} from "./Note/NoteEditor";
import EditorProvider from "../../../../context/EditorProvider";
import {ScheduleRowContext} from "../../../../context/ScheduleRowProvider";

const ScheduleRow = () => {
    const {row, rowNote} = useContext(ScheduleRowContext);
    const [editorMode, setrEditorMode] = useState(
        rowNote ? editorModes.display : editorModes.create
    );
    const [open, setOpen] = useState(false);
    const [showNoteBlock, setShowNoteBlock] = useState(false);

    const handleCollapse = () => {
        if (row.slice(1).join("") === "") return;

        if (!showNoteBlock) {
            setShowNoteBlock(true);
            setTimeout(() => setOpen(true), 1);
        } else {
            setOpen(false);
        }
    }

    return (
        <React.Fragment>
            <tr
                className={rowNote ? "cells-tr existing-note-tr" : "cells-tr"}
                onClick={handleCollapse}
                aria-expanded="false"
                role="button"
            >
                {row.map((cell, tdIndex) => (
                    <td key={tdIndex}>{cell}</td>
                ))}
            </tr>
            {showNoteBlock &&
                <tr>
                    <td className="note-block" colSpan="5" data-note-location="{{ note_location }}">
                        <Collapse
                            in={open}
                            onExited={() => setShowNoteBlock(false)}
                        >
                            <div>
                                <div className="card card-body note-block__card">
                                    <EditorProvider
                                        setOpen={setOpen}
                                        editorMode={editorMode}
                                        setEditorMode={setrEditorMode}
                                    >
                                        <NoteEditor/>
                                    </EditorProvider>
                                </div>
                            </div>
                        </Collapse>
                    </td>
                </tr>
            }
        </React.Fragment>
    );
};

export default ScheduleRow;