import React, {useContext} from 'react';
import PeriodForm from "../../../../components/Schedule/Content/PeriodForm/PeriodForm";
import {AuthContext} from "../../../../context/main/AuthProvider";

const GroupTitleBlock = () => {
    const {userData} = useContext(AuthContext);

    return (
        <div className="schedule__title-block flex">
            <h1 className="schedule__title title">{userData.group}</h1>
            <PeriodForm/>
        </div>
    );
};

export default GroupTitleBlock;