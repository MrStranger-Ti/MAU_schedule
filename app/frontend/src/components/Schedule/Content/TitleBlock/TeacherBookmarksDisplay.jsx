import React, {useContext} from "react";
import {TeacherBookmarksContext} from "../../../../context/schedule/TeacherBookmarksProvider";
import {Link} from "react-router-dom";
import {pagesPaths} from "../../../../AppRoutes";

const TeacherBookmarksDisplay = () => {
    const {teacherBookmarks} = useContext(TeacherBookmarksContext);

    return (
        <div className="dropdown schedule__bookmarks">
            <button className="btn-secondary dropdown-toggle schedule__bookmarks-btn" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                <svg version="1.0" width="512.000000pt" height="512.000000pt" viewBox="0 0 512.000000 512.000000" preserveAspectRatio="xMidYMid meet">
                    <g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)">
                        <path d="M2044 4895 c-34 -7 -81 -23 -104 -35 -55 -28 -143 -110 -174 -164
-29 -50 -56 -138 -56 -183 l0 -33 878 0 c711 0 887 -3 928 -14 155 -41 280
-171 313 -324 8 -37 11 -385 11 -1185 l0 -1132 213 -264 212 -264 3 1589 c1
989 -1 1613 -7 1652 -29 187 -172 332 -357 362 -35 6 -414 10 -929 9 -684 0
-883 -3 -931 -14z"/>
                        <path d="M1150 4031 c-30 -9 -73 -29 -95 -43 -53 -33 -128 -115 -155 -168 -51
-100 -50 -49 -50 -1889 0 -1567 1 -1713 16 -1707 9 3 298 175 642 382 l625
375 630 -378 c346 -208 634 -380 638 -381 5 -2 8 744 7 1755 l-3 1759 -37 75
c-46 93 -112 158 -206 202 l-67 32 -945 2 c-882 2 -949 1 -1000 -16z m1838
-1734 c1 -730 0 -1327 -2 -1327 -3 0 -193 113 -423 251 -230 139 -423 252
-429 252 -5 0 -197 -111 -425 -248 -228 -136 -417 -250 -421 -252 -5 -2 -8
595 -8 1326 l0 1331 853 -2 852 -3 3 -1328z"/>
                    </g>
                </svg>
            </button>
            <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                {teacherBookmarks.length > 0
                    ?
                    <React.Fragment>
                        {teacherBookmarks.map(bookmark =>
                            <li className="bookmarks-item flex">
                                <Link
                                    className="dropdown-item schedule__bookmark-link link"
                                    to={pagesPaths.schedule.getTeacherURL(bookmark.teacher_key)}
                                >
                                    {bookmark.teacher_name}
                                </Link>
                                <button className="btn schedule__bookmark-btn" type="button">
                                    <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
                                        <g id="cross">
                                            <line className="cls-1" x1="7" x2="25" y1="7" y2="25"/>
                                            <line className="cls-1" x1="7" x2="25" y1="25" y2="7"/>
                                        </g>
                                    </svg>
                                </button>
                            </li>
                        )}
                    </React.Fragment>
                    :
                    <li className="bookmarks-item"><p className="schedule__bookmarks-empty">Здесь будут отображаться сохраненные расписания</p></li>
                }
            </ul>
        </div>
    );
};

export default TeacherBookmarksDisplay;