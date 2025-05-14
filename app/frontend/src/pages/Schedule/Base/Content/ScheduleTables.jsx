import React, {useContext} from "react";
import {Link} from "react-router-dom";
import {config} from "../../../../config";
import {getFormattedDate, getWeekday} from "../../../../utils/date";
import ScheduleRow from "./ScheduleRow";
import {ScheduleContext} from "../../../../context/ScheduleProvider";
import ScheduleRowProvider from "../../../../context/ScheduleRowProvider";

const ScheduleTables = () => {
    const {scheduleName, scheduleKey, schedule, notes} = useContext(ScheduleContext);

    const getRowNote = (day, lessonNumber) => {
        return notes.find((note) =>
            note.schedule_name === scheduleName
            && note.schedule_key === scheduleKey
            && note.day === day
            && note.lesson_number === lessonNumber
        );
    }

    return (
        <React.Fragment>
            {Object.keys(schedule).length !== 0
                ?
                <div className="schedule__list">
                    {Object.entries(schedule).map(([day, dayTable], dayIndex) => (
                        <React.Fragment key={dayIndex}>
                            <div className="schedule__table-block">
                                <div className="schedule__table-title-block flex">
                                    <span className="schedule__table-descr">{getWeekday(day)}</span>
                                    <span className="schedule__table-descr">{getFormattedDate(day)}</span>
                                </div>
                                <table className="schedule__table">
                                    <thead></thead>
                                    <tbody>
                                    {dayTable.map((row, trIndex) => (
                                        <ScheduleRowProvider
                                            row={row}
                                            day={day}
                                            lessonNumber={trIndex + 1}
                                            note={getRowNote(day, trIndex + 1)}
                                            key={trIndex}
                                        >
                                            <ScheduleRow/>
                                        </ScheduleRowProvider>
                                    ))}
                                    </tbody>
                                </table>
                            </div>
                        </React.Fragment>
                    ))}
                </div>
                :
                <div className="schedule__info-block">
                    <p className="schedule__info">Расписание не найдено. Проверьте свои данные в профиле.</p>
                    <p className="schedule__info">
                        Также неполадки могут быть связаны с неработающим расписанием на <Link className="dark-link link" to={config.SCHEDULE_URL} target="_blank">сайте</Link> университета.
                    </p>
                </div>
            }
        </React.Fragment>
    );
};

export default ScheduleTables;