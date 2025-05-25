import React, {useContext, useEffect, useState} from "react";
import {EditorContext} from "../../../../../context/schedule/EditorProvider";
import CollapseBtn from "./CollapseBtn";
import LoadingButton from "../../../../UI/Button/LoadingButton";
import AdaptiveCollapseBtn from "./AdaptiveCollapseBtn";
import {ScheduleRowContext} from "../../../../../context/schedule/ScheduleRowProvider";

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
            <div className="note-block__btns flex">
                <div className="note-block__btns-block">
                    <CollapseBtn/>
                </div>
                <div className="note-block__btns-block">
                    <LoadingButton
                        isLoading={isBtnLoading}
                        showChildrenOnLoad={false}
                        className="btn"
                        type="submit"
                    >
                        Сохранить
                    </LoadingButton>
                    <button
                        className="btn"
                        type="button"
                        onClick={cancel}
                    >
                        Отмена
                    </button>
                </div>
            </div>
            <div className="note-block__adaptive-btns flex">
                <div className="note-block__btns-block">
                    <AdaptiveCollapseBtn/>
                </div>
                <div className="note-block__btns-adaptive-block">
                    <LoadingButton
                        isLoading={isBtnLoading}
                        className="btn"
                        type="submit"
                    >
                        <svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="100.000000pt" height="100.000000pt" viewBox="0 0 100.000000 100.000000" preserveAspectRatio="xMidYMid meet">
                            <g transform="translate(0.000000,100.000000) scale(0.100000,-0.100000)">
                                <path d="M100 900 c-19 -19 -20 -33 -20 -400 0 -367 1 -381 20 -400 19 -19 33
          -20 400 -20 367 0 381 1 400 20 19 19 20 33 20 333 l0 312 -88 88 -87 87 -313
          0 c-299 0 -313 -1 -332 -20z m140 -150 c0 -181 -17 -170 250 -170 265 0 250
          -10 250 162 l0 122 70 -69 70 -70 -2 -300 -3 -300 -57 -3 -58 -3 0 161 c0 217
          22 200 -260 200 -282 0 -260 17 -260 -200 l0 -161 -57 3 -58 3 -3 365 c-1 201
          0 371 3 377 3 8 25 13 60 13 l55 0 0 -130z m458 3 l-3 -128 -205 0 -205 0 -3
          128 -3 127 211 0 211 0 -3 -127z m20 -475 l3 -158 -221 0 -220 0 0 153 c0 85
          3 157 7 161 4 3 102 5 217 4 l211 -3 3 -157z"/>
                                <path d="M160 180 c0 -13 7 -20 20 -20 13 0 20 7 20 20 0 13 -7 20 -20 20 -13
          0 -20 -7 -20 -20z"/>
                                <path d="M800 180 c0 -13 7 -20 20 -20 13 0 20 7 20 20 0 13 -7 20 -20 20 -13
          0 -20 -7 -20 -20z"/>
                                <path d="M564 827 c-3 -8 -4 -47 -2 -88 l3 -74 45 0 45 0 0 85 0 85 -43 3
          c-29 2 -44 -1 -48 -11z m56 -77 c0 -27 -4 -50 -10 -50 -5 0 -10 23 -10 50 0
          28 5 50 10 50 6 0 10 -22 10 -50z"/>
                            </g>
                        </svg>
                    </LoadingButton>
                    <button className="btn" type="button" onClick={cancel}>
                        <svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="64.000000pt" height="64.000000pt" viewBox="0 0 64.000000 64.000000" preserveAspectRatio="xMidYMid meet">
                            <g transform="translate(0.000000,64.000000) scale(0.100000,-0.100000)">
                                <path d="M143 552 c-18 -11 -83 -96 -83 -108 0 -18 80 -114 95 -114 7 0 18 7
        25 15 10 12 9 20 -5 41 l-16 25 146 -3 147 -3 34 -37 c28 -32 34 -45 34 -84 0
        -88 -50 -133 -156 -142 -59 -4 -64 -7 -64 -28 0 -29 32 -39 98 -30 62 8 109
        34 146 80 56 68 45 200 -20 257 -48 42 -79 49 -225 49 l-141 0 16 25 c9 13 16
        29 16 34 0 15 -34 31 -47 23z"/>
                            </g>
                        </svg>
                    </button>
                </div>
            </div>
        </React.Fragment>
    );
};

export default UpdateBtns;