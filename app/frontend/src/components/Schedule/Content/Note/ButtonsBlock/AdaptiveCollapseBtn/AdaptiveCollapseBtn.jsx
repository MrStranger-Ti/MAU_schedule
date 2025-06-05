import React, {useContext} from "react";
import Button from "../../../../../UI/Buttons/Button/Button";
import {NoteCollapseContext} from "../../../../../../context/schedule/NoteCollapseProvider";
import {ReactComponent as CollapseIcon} from "../../../../../../assets/icons/collapse.svg";
import buttonBlockStyles from "../ButtonsBlock.module.css";

const AdaptiveCollapseBtn = () => {
    const {handleCollapse} = useContext(NoteCollapseContext);

    return (
        <Button
            className={buttonBlockStyles.adaptiveButton}
            type="button"
            onClick={handleCollapse}
        >
            <CollapseIcon className={buttonBlockStyles.adaptiveIcon}/>
        </Button>
    );
};

export default AdaptiveCollapseBtn;