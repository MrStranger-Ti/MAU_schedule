import React, {useContext} from "react";
import {EditorContext} from "../../../../../../context/schedule/EditorProvider";
import CollapseBtn from "../CollapseBtn/CollapseBtn";
import LoadingButton from "../../../../../UI/Buttons/LoadingButton/LoadingButton";
import AdaptiveCollapseBtn from "../AdaptiveCollapseBtn/AdaptiveCollapseBtn";
import Button from "../../../../../UI/Buttons/Button/Button";
import {ReactComponent as EditIcon} from "../../../../../../assets/icons/edit.svg";
import {ReactComponent as DeleteIcon} from "../../../../../../assets/icons/delete1.svg";
import buttonsBlockStyles from "../ButtonsBlock.module.css";

const DisplayBtns = ({isBtnLoading}) => {
    const {setEditorMode, editorModes} = useContext(EditorContext);

    return (
        <React.Fragment>
            <div className={buttonsBlockStyles.buttons}>
                <div className={buttonsBlockStyles.buttonsBlock}>
                    <CollapseBtn/>
                </div>
                <div className={buttonsBlockStyles.buttonsBlock}>
                    <Button
                        type="button"
                        onClick={() => setEditorMode(editorModes.update)}
                    >
                        Редактировать
                    </Button>
                    <LoadingButton isLoading={isBtnLoading} type="submit">
                        Удалить
                    </LoadingButton>
                </div>
            </div>
            <div className={buttonsBlockStyles.adaptiveButtons}>
                <div className={buttonsBlockStyles.buttonsAdaptiveBlock}>
                    <AdaptiveCollapseBtn/>
                </div>
                <div className={buttonsBlockStyles.buttonsAdaptiveBlock}>
                    <Button
                        className={buttonsBlockStyles.adaptiveButton}
                        type="button"
                        onClick={() => setEditorMode(editorModes.update)}
                    >
                        <EditIcon
                            className={`${buttonsBlockStyles.adaptiveIcon} ${buttonsBlockStyles.editIcon}`}
                        />
                    </Button>
                    <LoadingButton
                        className={buttonsBlockStyles.adaptiveButton}
                        spinnerClassName={buttonsBlockStyles.buttonSpinner}
                        isLoading={isBtnLoading}
                        showChildrenOnLoad={false}
                        dark={true}
                        type="submit"
                        disabled={isBtnLoading && true}
                    >
                        <DeleteIcon
                            className={`${buttonsBlockStyles.adaptiveIcon} ${buttonsBlockStyles.deleteIcon}`}
                        />
                    </LoadingButton>
                </div>
            </div>
        </React.Fragment>
    );
};

export default DisplayBtns;