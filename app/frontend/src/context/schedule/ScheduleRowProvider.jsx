import React, {createContext, useState} from "react";

export const ScheduleRowContext = createContext(null);

export const ScheduleRowProvider = ({
                                        children,
                                        row,
                                        day,
                                        lessonNumber,
                                        note
                                    }) => {
    const [rowNote, setRowNote] = useState(note);
    const [openCollapse, setOpenCollapse] = useState(false);
    const [showNoteBlock, setShowNoteBlock] = useState(false);

    const handleCollapse = () => {
        if (row.slice(1).join("") === "") return;

        if (!showNoteBlock) {
            setShowNoteBlock(true);
            setTimeout(() => setOpenCollapse(true), 1);
        } else {
            setOpenCollapse(false);
        }
    }

    return (
        <ScheduleRowContext.Provider value={{
            row,
            day,
            lessonNumber,
            rowNote,
            setRowNote,
            handleCollapse,
            openCollapse,
            setOpenCollapse,
            showNoteBlock,
            setShowNoteBlock
        }}>
            {children}
        </ScheduleRowContext.Provider>
    );
};

export default ScheduleRowProvider;