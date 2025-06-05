import React from "react";
import NoteCollapseProvider from "../../../../context/schedule/NoteCollapseProvider";
import NoteRow from "../Note/NoteRow/NoteRow";
import ScheduleRow from "../ScheduleRow/ScheduleRow";

const ScheduleLesson = () => {
    return (
        <NoteCollapseProvider>
            <ScheduleRow/>
            <NoteRow/>
        </NoteCollapseProvider>
    );
};

export default ScheduleLesson;