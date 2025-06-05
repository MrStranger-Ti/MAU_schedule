import React, {useContext} from "react";
import {NoteCollapseContext} from "../../../../../../context/schedule/NoteCollapseProvider";
import Button from "../../../../../UI/Buttons/Button/Button";

const CollapseBtn = () => {
    const {handleCollapse} = useContext(NoteCollapseContext);

    return (
        <Button type="button" onClick={handleCollapse}>
            Свернуть
        </Button>
    );
};

export default CollapseBtn;