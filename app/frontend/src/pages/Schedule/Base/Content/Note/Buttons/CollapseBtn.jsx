import React from "react";

const CollapseBtn = ({onClickCollapse}) => {
    return (
        <button
            className="btn"
            type="button"
            onClick={onClickCollapse}
        >Свернуть</button>
    );
};

export default CollapseBtn;