import React, {createContext, useState} from 'react';
import NotificationsBlock from "../../components/UI/Notification/NotificationsBlock";
import {v4 as getUniqueKey} from "uuid";

export const NotificationContext = createContext(null);

const NotificationProvider = ({children}) => {
    const [notifications, setNotifications] = useState([]);

    const showNotification = (text, {error = false} = {}) => {
        setNotifications([...notifications, {
            key: getUniqueKey(),
            text,
            error
        }]);
    }

    const removeNotification = (key) => {
        setNotifications(notifications.filter(
            notification => notification.key !== key)
        )
    }

    return (
        <NotificationContext value={{showNotification, notifications, removeNotification}}>
            {children}
            <NotificationsBlock/>
        </NotificationContext>
    );
};

export default NotificationProvider;