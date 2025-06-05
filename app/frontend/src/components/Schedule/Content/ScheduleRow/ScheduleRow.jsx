import React, {useContext} from "react";
import {NotesContext} from "../../../../context/schedule/NotesProvider";
import {ScheduleRowContext} from "../../../../context/schedule/ScheduleRowProvider";
import {NoteCollapseContext} from "../../../../context/schedule/NoteCollapseProvider";
import styles from "./ScheduleRow.module.css";

const ScheduleRow = () => {
    const {notes} = useContext(NotesContext);
    const {row, rowNote} = useContext(ScheduleRowContext);
    const {handleCollapse} = useContext(NoteCollapseContext);

    return (
        <tr
            className={
                rowNote && notes.some(note => note.id === rowNote.id)
                    ? `${styles.cellsRow} ${styles.existingNoteTr}`
                    : styles.cellsRow
            }
            onClick={handleCollapse}
        >
            {row.map((cell, tdIndex) => (
                <td key={tdIndex}>{cell}</td>
            ))}
        </tr>
    );
};

export default ScheduleRow;