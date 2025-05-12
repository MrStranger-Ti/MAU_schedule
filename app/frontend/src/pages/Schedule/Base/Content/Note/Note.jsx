import React, {useState} from "react";
import Form from "../../../../../components/UI/Form/Form";
import SunEditor from "suneditor-react";
import DisplayBtns from "./Buttons/DisplayBtns";
import CreateBtns from "./Buttons/CreateBtns";
import UpdateBtns from "./Buttons/UpdateBtns";

const sunEditorOptions = {
    width: "100%",
    height: "100%",
    maxHeight: "1000px",
    resizingBar: false,
    minHeight: "200px",
    font: ["Montserrat"],
    className: "note-block__editable",
    buttonList: [
        ["undo", "redo"],
        [":p-More Paragraph-default.more_paragraph", "bold", "underline", "italic", "strike"],
        ["textStyle"],
        ["align", "list"],
        ["fullScreen"]
    ]
};

const editorModes = {
    display: "display",
    create: "create",
    update: "update"
};

const Note = ({setOpen}) => {
    const [editorMode, setrEditorMode] = useState(editorModes.display);

    const onClickCollapse = () => setOpen(false);

    const ButtonsGroups = {
        display: <DisplayBtns
            onClickCollapse={onClickCollapse}
        />,
        create: <CreateBtns
            onClickCollapse={onClickCollapse}
        />,
        update: <UpdateBtns
            onClickCollapse={onClickCollapse}
        />
    };

    const ButtonsComponent = ButtonsGroups[editorMode];

    return (
        <Form className="note-block__form flex">
            <SunEditor setOptions={sunEditorOptions} lang="ru"/>
            {ButtonsComponent}
        </Form>
    );
};

export default Note;