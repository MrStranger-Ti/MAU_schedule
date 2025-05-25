import React, {useContext} from 'react';
import TitleForm from "./TitleForm";
import {AuthContext} from "../../../../context/AuthProvider";

const TitleBlock = () => {
    const {userData} = useContext(AuthContext);

    return (
        <div className="schedule__title-block flex">
            <h1 className="schedule__title title">{userData.group}</h1>
            <TitleForm/>
        </div>
    );
};

export default TitleBlock;