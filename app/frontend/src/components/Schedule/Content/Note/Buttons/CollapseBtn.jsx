import React, {useContext} from "react";
import {NoteCollapseContext} from "../../../../../context/schedule/NoteCollapseProvider";

const CollapseBtn = () => {
    const {handleCollapse} = useContext(NoteCollapseContext);

    return (
        <button
            className="btn"
            type="button"
            onClick={handleCollapse}
        >Свернуть</button>
    );
};

export default CollapseBtn;