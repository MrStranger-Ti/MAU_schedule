import React, {useContext} from "react";
import {NotesContext} from "../../../../context/schedule/NotesProvider";
import {ScheduleRowContext} from "../../../../context/schedule/ScheduleRowProvider";
import {NoteCollapseContext} from "../../../../context/schedule/NoteCollapseProvider";

const ScheduleRow = () => {
    const {notes} = useContext(NotesContext);
    const {row, rowNote} = useContext(ScheduleRowContext);
    const {handleCollapse} = useContext(NoteCollapseContext);

    return (
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
    );
};

export default ScheduleRow;