import React, {useContext} from "react";
import {Collapse} from "react-bootstrap";
import NoteEditor from "../NoteEditor/NoteEditor";
import {NoteCollapseContext} from "../../../../../context/schedule/NoteCollapseProvider";
import EditorProvider from "../../../../../context/schedule/EditorProvider";
import styles from "./NoteRow.module.css";

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
                    <td className={styles.noteBlock} colSpan="5">
                        <Collapse
                            in={isOpenCollapse}
                            onEnter={handleOnEnter}
                            onEntered={handleOnEntered}
                            onExit={handleOnExit}
                            onExited={handleOnExited}
                        >
                            <div>
                                <div className={styles.editorBlock}>
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