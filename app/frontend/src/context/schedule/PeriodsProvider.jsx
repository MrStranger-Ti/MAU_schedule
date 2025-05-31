import React, {createContext, useContext, useState} from "react";
import ScheduleService from "../../services/schedule";
import {NotificationContext} from "../main/NotificationProvider";

export const PeriodsContext = createContext(null);

const PeriodsProvider = ({children}) => {
    const {showNotification} = useContext(NotificationContext);
    const [periods, setPeriods] = useState([]);
    const [currentPeriodValue, setCurrentPeriodValue] = useState("");
    const [isPeriodsLoaded, setIsPeriodLoaded] = useState(false);

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

        setIsPeriodLoaded(true);
    }

    return (
        <PeriodsContext.Provider value={{
            fetchPeriods, isPeriodsLoaded,
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