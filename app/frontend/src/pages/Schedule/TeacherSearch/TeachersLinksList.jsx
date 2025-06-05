import React from "react";
import {Link} from "react-router-dom";
import {pagesPaths} from "../../../AppRoutes";
import {config} from "../../../config";

const TeachersLinksList = ({teachersKeys}) => {
    return (
        <React.Fragment>
            {teachersKeys.length > 0
                ?
                <ul className="schedule__teacher-links">
                    {teachersKeys.map(item =>
                        <li key={item.teacherKey}>
                            <Link
                                className="dark-link link"
                                to={pagesPaths.schedule.getTeacherURL(item.key, item.name)}
                            >
                                {item.name}
                            </Link>
                        </li>
                    )}
                </ul>
                :
                <div className="schedule__info-block">
                    <p className="schedule__info">Ни одного преподавателя не найдено.</p>
                    <p className="schedule__info">
                        Неполадки могут быть связаны с неработающим расписанием на <Link className="dark-link link" to={config.SCHEDULE_URL} target="_blank">сайте&nbsp;университета</Link>.
                    </p>
                </div>
            }
        </React.Fragment>
    );
};

export default TeachersLinksList;