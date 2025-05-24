import React, {createContext} from "react";

export const EditorContext = createContext(null);

export const EditorProvider = ({
                                   children,
                                   setOpen,
                                   editorMode,
                                   setEditorMode
                               }) => {
    return (
        <EditorContext.Provider value={{setOpen, editorMode, setEditorMode}}>
            {children}
        </EditorContext.Provider>
    );
};

export default EditorProvider;