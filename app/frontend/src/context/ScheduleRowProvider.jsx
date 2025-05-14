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
    return (
        <ScheduleRowContext.Provider value={{row, day, lessonNumber, rowNote, setRowNote}}>
            {children}
        </ScheduleRowContext.Provider>
    );
};

export default ScheduleRowProvider;