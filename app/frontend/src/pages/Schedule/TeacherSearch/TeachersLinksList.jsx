import React from "react";
import {Link} from "react-router-dom";
import {pagesPaths} from "../../../AppRoutes";

const TeachersLinksList = ({teachersKeys}) => {
    return (
        <React.Fragment>
            {teachersKeys.length > 0
                ?
                <ul className="schedule__teacher-links">
                    {teachersKeys.map(item =>
                        <li>
                            <Link
                                className="dark-link link"
                                to={pagesPaths.schedule.getTeacherURL(item.key)}
                            >
                                {item.name}
                            </Link>
                        </li>
                    )}
                </ul>
                :
                <div className="schedule__info-block">
                    <p className="schedule__info">Ни одного преподавателя не найдено.</p>
                </div>
            }
        </React.Fragment>
    );
};

export default TeachersLinksList;