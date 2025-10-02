import React, {useContext} from "react";
import {Link} from "react-router-dom";
import {ScheduleContext} from "../../context/schedule/ScheduleProvider";
import {NotesContext} from "../../context/schedule/NotesProvider";
import {getFormattedDate, getWeekday} from "../../utils/date";
import ScheduleRowProvider from "../../context/schedule/ScheduleRowProvider";
import {config} from "../../config";
import Spinner from "../Spinner/Spinner";
import ScheduleLesson from "./Content/ScheduleLesson/ScheduleLesson";
import scheduleStyles from "../../styles/pages/Schedule.module.css";
import styles from "./Schedule.module.css";

const Schedule = () => {
    const {
        scheduleName, scheduleKey,
        schedule, isScheduleLoading
    } = useContext(ScheduleContext);
    const {notes} = useContext(NotesContext);

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
            {isScheduleLoading
                ?
                <Spinner/>
                :
                <React.Fragment>
                    {Object.keys(schedule).length !== 0
                        ?
                        <div className={styles.schedule}>
                            {Object.entries(schedule).map(([day, dayTable], dayIndex) => (
                                <React.Fragment key={dayIndex}>
                                    <div className={styles.tableBlock}>
                                        <div className={styles.titleBlock}>
                                            <span className={styles.descr}>{getWeekday(day)}</span>
                                            <span className={styles.descr}>{getFormattedDate(day)}</span>
                                        </div>
                                        <table className={styles.table}>
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
                                                    <ScheduleLesson/>
                                                </ScheduleRowProvider>
                                            ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </React.Fragment>
                            ))}
                        </div>
                        :
                        <div className={scheduleStyles.infoBlock}>
                            <p className={scheduleStyles.info}>Расписание не найдено. Проверьте свои данные в профиле.</p>
                            <p className={scheduleStyles.info}>
                                Неполадки могут быть связаны с неработающим расписанием на <Link className="dark-link link" to={config.SCHEDULE_URL} target="_blank">сайте&nbsp;университета</Link>.
                            </p>
                        </div>
                    }
                </React.Fragment>
            }
        </React.Fragment>
    );
};

export default Schedule;