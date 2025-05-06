import React from "react";

const ScheduleTable = ({schedule}) => {
    const getScheduleWeekday = (dateString) => {
        const daysOfWeek = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'];
        const date = new Date(dateString);
        const dayIndex = date.getDay();
        return daysOfWeek[dayIndex];
    }

    const getFormattedDate = (dateString) => {
        const [year, month, day] = dateString.split("-");
        return `${day}-${month}-${year}`;
    }

    return (
        <div className="schedule__list">
            {Object.entries(schedule).map(([date, day_table], index) => (
                <React.Fragment key={index}>
                    <div className="schedule__table-block">
                        <div className="schedule__table-title-block flex">
                            <span className="schedule__table-descr">{getScheduleWeekday(date)}</span>
                            <span className="schedule__table-descr">{getFormattedDate(date)}</span>
                        </div>
                        <table className="schedule__table">
                            <thead></thead>
                            <tbody>
                            {day_table.map((row, index) => (
                                <tr key={index}>
                                    {row.map((cell, index) => (
                                        <td key={index}>{cell}</td>
                                    ))}
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                </React.Fragment>
            ))}
        </div>
    );
};

export default ScheduleTable;