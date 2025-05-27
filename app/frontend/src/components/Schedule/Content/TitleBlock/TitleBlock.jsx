import React, {useContext} from 'react';
import {ScheduleContext} from "../../../../context/schedule/ScheduleProvider";
import GroupTitleBlock from "./GroupTitleBlock";
import TeacherTitleBlock from "./TeacherTitleBlock";

const TitleBlock = () => {
    const {scheduleName} = useContext(ScheduleContext);

    const renderTitleBlock = () => {
        let titleBlock = null;
        switch (scheduleName) {
            case "group":
                titleBlock = <GroupTitleBlock/>;
                break;
            case "teacher":
                titleBlock = <TeacherTitleBlock/>;
                break;
            default:
                throw new Error(`Invalid scheduleName: ${scheduleName}`);
        }
        return titleBlock;
    }

    return (
        <React.Fragment>
            {renderTitleBlock()}
        </React.Fragment>
    );
};

export default TitleBlock;