import {createContext, useContext, useState} from "react";
import {ScheduleRowContext} from "./ScheduleRowProvider";

export const NoteCollapseContext = createContext(null);

const NoteCollapseProvider = ({children}) => {
    const {row} = useContext(ScheduleRowContext);
    const [showNoteBlock, setShowNoteBlock] = useState(false);
    const [isOpenCollapse, setIsOpenCollapse] = useState(false);
    const [isAnimatingCollapse, setIsAnimatingCollapse] = useState(false);

    const handleCollapse = () => {
        if (row.slice(1).join("") === "") return;

        if (!showNoteBlock) {
            if (!isAnimatingCollapse) {
                setShowNoteBlock(true);
                setTimeout(() => setIsOpenCollapse(true), 1);
            }
        } else {
            if (!isAnimatingCollapse) {
                setIsOpenCollapse(false);
            }
        }
    }

    const handleOnEnter = () => setIsAnimatingCollapse(true);
    const handleOnEntered = () => {
        setTimeout(() => setIsAnimatingCollapse(false), 100);
    }
    const handleOnExit = () => setIsAnimatingCollapse(true);
    const handleOnExited = () => {
        setIsAnimatingCollapse(false);
        setShowNoteBlock(false);
    }


    return (
        <NoteCollapseContext.Provider value={{
            handleCollapse,
            handleOnEnter, handleOnEntered,
            handleOnExit, handleOnExited,
            showNoteBlock, setShowNoteBlock,
            isOpenCollapse
        }}>
            {children}
        </NoteCollapseContext.Provider>
    );
};

export default NoteCollapseProvider;