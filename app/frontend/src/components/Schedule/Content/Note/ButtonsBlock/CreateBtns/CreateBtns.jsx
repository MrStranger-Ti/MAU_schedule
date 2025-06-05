import React from "react";
import CollapseBtn from "../CollapseBtn/CollapseBtn";
import LoadingButton from "../../../../../UI/Buttons/LoadingButton/LoadingButton";
import AdaptiveCollapseBtn from "../AdaptiveCollapseBtn/AdaptiveCollapseBtn";
import buttonsBlockStyles from "../ButtonsBlock.module.css";
import {ReactComponent as CreateIcon} from "../../../../../../assets/icons/save.svg";

const CreateBtns = ({isBtnLoading}) => {
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
                        <CreateIcon className={`${buttonsBlockStyles.adaptiveIcon} ${buttonsBlockStyles.saveIcon}`}/>
                    </LoadingButton>
                </div>
            </div>
        </React.Fragment>
    );
};

export default CreateBtns;