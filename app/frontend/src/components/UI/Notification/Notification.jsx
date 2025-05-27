import React, {useContext, useEffect, useState} from "react";
import {NotificationContext} from "../../../context/main/NotificationProvider";

const Notification = ({notification}) => {
    const {removeNotification} = useContext(NotificationContext);
    const [show, setShow] = useState(true);
    const [opacity, setOpacity] = useState("1");

    useEffect(() => {
        setTimeout(() => setOpacity("0"), 5000);
    }, []);

    useEffect(() => {
        if (opacity === "0") {
            setTimeout(() => setShow(false), 300)
        }
    }, [opacity]);

    useEffect(() => {
        if (!show) removeNotification(notification.key);
    }, [show]);

    return (
        <div className="notification__block flex" style={{opacity}}>
            <div className={notification.error ? "notification__icon-error" : "notification__icon-ok"}></div>
            <p className="notification__descr">
                {notification.text}
            </p>
        </div>
    );
};

export default Notification;