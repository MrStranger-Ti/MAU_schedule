import React, {useContext} from "react";
import Notification from "./Notification";
import {NotificationContext} from "../../../context/NotificationProvider";

const NotificationsBlock = () => {
    const {notifications} = useContext(NotificationContext);

    return (
        <div className="notification flex">
            {notifications.map(notification => (
                <Notification notification={notification} key={notification.key}/>
            ))}
        </div>
    );
};

export default NotificationsBlock;