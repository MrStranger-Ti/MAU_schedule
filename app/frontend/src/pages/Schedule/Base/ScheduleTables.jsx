import React from "react";
import {Link} from "react-router-dom";
import {config} from "../../../config";
import {getFormattedDate, getWeekday} from "../../../utils/date";
import NoteCollapse from "./NoteCollapse";
import ScheduleRow from "./ScheduleRow";

const ScheduleTables = ({schedule}) => {
    return (
        <React.Fragment>
            {Object.keys(schedule).length !== 0
                ?
                <div className="schedule__list">
                    {Object.entries(schedule).map(([date, day_table], day_index) => (
                        <React.Fragment key={day_index}>
                            <div className="schedule__table-block">
                                <div className="schedule__table-title-block flex">
                                    <span className="schedule__table-descr">{getWeekday(date)}</span>
                                    <span className="schedule__table-descr">{getFormattedDate(date)}</span>
                                </div>
                                <table className="schedule__table">
                                    <thead></thead>
                                    <tbody>
                                    {day_table.map((row, tr_index) => (
                                        <ScheduleRow
                                            row={row}
                                            collapseId={`collapse-${day_index}-${tr_index}`}
                                            key={tr_index}
                                        />
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