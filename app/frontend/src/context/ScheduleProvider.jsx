import React, {createContext} from "react";

export const ScheduleContext = createContext(null);

const ScheduleProvider = ({
                              children,
                              scheduleName,
                              scheduleKey,
                              fetchSchedule,
                              isScheduleLoading,
                              setIsScheduleLoading,
                              schedule,
                              periods,
                              currentPeriodValue,
                              setCurrentPeriodValue,
                              notes,
                              setNotes
                          }) => {
    return (
        <ScheduleContext.Provider value={{
            scheduleName,
            scheduleKey,
            fetchSchedule,
            isScheduleLoading,
            setIsScheduleLoading,
            schedule,
            periods,
            currentPeriodValue,
            setCurrentPeriodValue,
            notes,
            setNotes
        }}>
            {children}
        </ScheduleContext.Provider>
    );
};

export default ScheduleProvider;