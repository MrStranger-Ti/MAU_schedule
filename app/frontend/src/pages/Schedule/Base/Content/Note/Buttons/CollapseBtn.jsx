import React, {useContext} from "react";
import {EditorContext} from "../../../../../../context/EditorProvider";

const CollapseBtn = () => {
    const {setOpen} = useContext(EditorContext);

    return (
        <button
            className="btn"
            type="button"
            onClick={() => setOpen(false)}
        >Свернуть</button>
    );
};

export default CollapseBtn;