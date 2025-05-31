import React, {useContext} from "react";
import {Collapse} from "react-bootstrap";
import {ScheduleRowContext} from "../../../context/schedule/ScheduleRowProvider";
import NoteEditor from "../Content/Note/NoteEditor";
import EditorProvider from "../../../context/schedule/EditorProvider";
import {NotesContext} from "../../../context/schedule/NotesProvider";

const ScheduleRow = () => {
    const {notes} = useContext(NotesContext);
    const {
        row, rowNote,
        handleCollapse,
        showNoteBlock, setShowNoteBlock,
        openCollapse
    } = useContext(ScheduleRowContext);

    return (
        <React.Fragment>
            <tr
                className={
                    rowNote && notes.some(note => note.id === rowNote.id)
                        ? "cells-tr existing-note-tr"
                        : "cells-tr"
                }
                onClick={handleCollapse}
                aria-expanded="false"
                role="button"
            >
                {row.map((cell, tdIndex) => (
                    <td key={tdIndex}>{cell}</td>
                ))}
            </tr>
            <EditorProvider>
                {showNoteBlock &&
                    <tr>
                        <td className="note-block" colSpan="5" data-note-location="{{ note_location }}">
                            <Collapse
                                in={openCollapse}
                                onExited={() => setShowNoteBlock(false)}
                            >
                                <div>
                                    <div className="card card-body note-block__card">
                                        <NoteEditor/>
                                    </div>
                                </div>
                            </Collapse>
                        </td>
                    </tr>
                }
            </EditorProvider>
        </React.Fragment>
    );
};

export default ScheduleRow;