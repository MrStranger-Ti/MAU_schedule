import React, {useState} from "react";
import {Collapse} from "react-bootstrap";
import Note from "./Note/Note";

const ScheduleRow = ({row}) => {
    const [open, setOpen] = useState(false);
    const [showNoteBlock, setShowNoteBlock] = useState(false);

    const handleCollapse = () => {
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
                className="cells-tr"
                onClick={handleCollapse}
                aria-expanded="false"
                role="button"
            >
                {row.map((cell, td_index) => (
                    <td key={td_index}>{cell}</td>
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
                                    <Note setOpen={setOpen}/>
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