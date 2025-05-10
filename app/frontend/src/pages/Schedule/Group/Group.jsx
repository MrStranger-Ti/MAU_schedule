import React from "react";
import BaseSchedule from "../BaseSchedule";
import Auth from "../../../components/Auth/Auth";
import Schedule from "../Base/Schedule";

const Group = () => {
    return (
        <Auth stopLoading={false} protect={true}>
            <BaseSchedule>
                <Schedule/>
            </BaseSchedule>
        </Auth>
    );
};

export default Group;