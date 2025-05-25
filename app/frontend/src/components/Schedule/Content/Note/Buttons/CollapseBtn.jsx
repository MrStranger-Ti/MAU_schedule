import React, {useContext} from "react";
import {ScheduleRowContext} from "../../../../../context/schedule/ScheduleRowProvider";

const CollapseBtn = () => {
    const {handleCollapse} = useContext(ScheduleRowContext);

    return (
        <button
            className="btn"
            type="button"
            onClick={handleCollapse}
        >Свернуть</button>
    );
};

export default CollapseBtn;