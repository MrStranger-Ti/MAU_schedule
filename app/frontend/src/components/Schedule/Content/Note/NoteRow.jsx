import React, {useContext} from "react";
import {Collapse} from "react-bootstrap";
import NoteEditor from "./NoteEditor";
import {NoteCollapseContext} from "../../../../context/schedule/NoteCollapseProvider";
import EditorProvider from "../../../../context/schedule/EditorProvider";

const NoteRow = () => {
    const {
        handleOnEnter, handleOnEntered,
        handleOnExit, handleOnExited,
        showNoteBlock, isOpenCollapse
    } = useContext(NoteCollapseContext);

    return (
        <EditorProvider>
            {showNoteBlock &&
                <tr>
                    <td className="note-block" colSpan="5">
                        <Collapse
                            in={isOpenCollapse}
                            onEnter={handleOnEnter}
                            onEntered={handleOnEntered}
                            onExit={handleOnExit}
                            onExited={handleOnExited}
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
    );
};

export default NoteRow;