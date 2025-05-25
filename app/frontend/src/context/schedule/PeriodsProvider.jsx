import React, {createContext, useContext, useState} from "react";
import ScheduleService from "../../services/schedule";
import {NotificationContext} from "../NotificationProvider";

export const PeriodsContext = createContext(null);

const PeriodsProvider = ({children}) => {
    const {showNotification} = useContext(NotificationContext);
    const [periods, setPeriods] = useState([]);
    const [currentPeriodValue, setCurrentPeriodValue] = useState("");

    const fetchPeriods = async () => {
        const service = new ScheduleService();
        const {success, data} = await service.getPeriods();
        if (success) {
            setPeriods(
                data.map((period, index) =>
                    ({name: period, value: index})
                )
            );
        } else {
            showNotification(data.detail, {error: true});
        }
    }

    return (
        <PeriodsContext.Provider value={{
            fetchPeriods,
            periods,
            setPeriods,
            currentPeriodValue,
            setCurrentPeriodValue
        }}>
            {children}
        </PeriodsContext.Provider>
    );
};

export default PeriodsProvider;