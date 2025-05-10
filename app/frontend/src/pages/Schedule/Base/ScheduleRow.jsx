import React, {useState} from "react";
import NoteCollapse from "./NoteCollapse";
import {Collapse} from "react-bootstrap";

const ScheduleRow = ({row, collapseId}) => {
    const [open, setOpen] = useState(false);

    return (
        <React.Fragment>
            <tr
                className="cell-tr"
                onClick={() => setOpen(!open)}
                aria-expanded="false"
                role="button"
            >
                {row.map((cell, td_index) => (
                    <td key={td_index}>{cell}</td>
                ))}
            </tr>
            <Collapse in={open}>
                <tr>
                    <td className="note-block" colSpan="5" data-note-location="{{ note_location }}">
                        <NoteCollapse/>
                    </td>
                </tr>
            </Collapse>
        </React.Fragment>
    );
};

export default ScheduleRow;