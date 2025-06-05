import React, {useContext, useEffect, useState} from "react";
import {EditorContext} from "../../../../../../context/schedule/EditorProvider";
import CollapseBtn from "../CollapseBtn/CollapseBtn";
import LoadingButton from "../../../../../UI/Buttons/LoadingButton/LoadingButton";
import AdaptiveCollapseBtn from "../AdaptiveCollapseBtn/AdaptiveCollapseBtn";
import {ScheduleRowContext} from "../../../../../../context/schedule/ScheduleRowProvider";
import Button from "../../../../../UI/Buttons/Button/Button";
import {ReactComponent as SaveIcon} from "../../../../../../assets/icons/save.svg";
import {ReactComponent as BackIcon} from "../../../../../../assets/icons/back.svg";
import buttonsBlockStyles from "../ButtonsBlock.module.css";


const UpdateBtns = ({isBtnLoading}) => {
    const {rowNote} = useContext(ScheduleRowContext);
    const {
        editorModes, editorRef,
        setEditorMode,
        editorText, setEditorText,
    } = useContext(EditorContext);
    const [isCancelClicked, setIsCancelClicked] = useState(false);

    useEffect(() => {
        if (isCancelClicked) {
            const currentEditorText = editorRef.current.getContents();
            if (currentEditorText !== rowNote.text) {
                setEditorText(rowNote.text);
            } else {
                setEditorMode(editorModes.display);
            }
        }

    }, [isCancelClicked, editorText]);

    const cancel = () => setIsCancelClicked(true);

    return (
        <React.Fragment>
            <div className={buttonsBlockStyles.buttons}>
                <div className={buttonsBlockStyles.buttonsBlock}>
                    <CollapseBtn/>
                </div>
                <div className={buttonsBlockStyles.buttonsBlock}>
                    <LoadingButton isLoading={isBtnLoading} type="submit">
                        Сохранить
                    </LoadingButton>
                    <Button type="button" onClick={cancel}>
                        Отмена
                    </Button>
                </div>
            </div>
            <div className={buttonsBlockStyles.adaptiveButtons}>
                <div className={buttonsBlockStyles.buttonsAdaptiveBlock}>
                    <AdaptiveCollapseBtn/>
                </div>
                <div className={buttonsBlockStyles.buttonsAdaptiveBlock}>
                    <LoadingButton
                        className={buttonsBlockStyles.adaptiveButton}
                        spinnerClassName={buttonsBlockStyles.buttonSpinner}
                        isLoading={isBtnLoading}
                        showChildrenOnLoad={false}
                        dark={true}
                        type="submit"
                        disabled={isBtnLoading && true}
                    >
                        <SaveIcon
                            className={`${buttonsBlockStyles.adaptiveIcon} ${buttonsBlockStyles.saveIcon}`}
                        />
                    </LoadingButton>
                    <Button
                        className={buttonsBlockStyles.adaptiveButton}
                        type="button"
                        onClick={cancel}
                    >
                        <BackIcon
                            className={`${buttonsBlockStyles.adaptiveIcon} ${buttonsBlockStyles.backIcon}`}
                        />
                    </Button>
                </div>
            </div>
        </React.Fragment>
    );
};

export default UpdateBtns;