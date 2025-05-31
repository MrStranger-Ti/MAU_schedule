import React from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import IndexPage from "./pages/IndexPage";
import Profile from "./pages/Profile/Profile";
import Login from "./pages/Auth/Login/Login";
import Register from "./pages/Auth/Register/Register";
import RegisterConfirm from "./pages/Auth/RegisterConfirm/RegisterConfirm";
import PasswordReset from "./pages/Auth/PasswordReset/PasswordReset";
import PasswordResetConfirm from "./pages/Auth/PasswordResetConfirm/PasswordResetConfirm";
import TeacherSearch from "./pages/Schedule/TeacherSearch/TeacherSearch";
import GroupSchedulePage from "./pages/Schedule/Group/GroupSchedulePage/GroupSchedulePage";
import TeacherSchedulePage from "./pages/Schedule/Teacher/TeacherSchedulePage/TeacherSchedulePage";

export const pagesPaths = {
    index: "/",
    accounts: {
        login: "/accounts/login/",
        register: "/accounts/register/",
        baseRegisterConfirm: "/accounts/register/confirm/",
        registerConfirm: "/accounts/register/confirm/:uidb64/:token/",
        passwordReset: "/accounts/password-reset/",
        basePasswordResetConfirm: "/accounts/password-reset/confirm/",
        passwordResetConfirm: "/accounts/password-reset/confirm/:uidb64/:token/",
        profile: "/accounts/profile/",
    },
    schedule: {
        group: "/schedule/group/",
        teacherSearch: "/schedule/teacher-search/",
        teacher: `/schedule/teacher/:keyName/`,
        getTeacherURL: (key, name) => {
            const encodedKeyName = encodeURIComponent(key + "~" + name);
            return `/schedule/teacher/${encodedKeyName}/`;
        }
    }
}

const AppRoutes = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path={pagesPaths.index}
                    element={<IndexPage/>}
                />
                <Route
                    path={pagesPaths.accounts.login}
                    element={<Login/>}
                />
                <Route
                    path={pagesPaths.accounts.register}
                    element={<Register/>}
                />
                <Route
                    path={pagesPaths.accounts.registerConfirm}
                    element={<RegisterConfirm/>}
                />
                <Route
                    path={pagesPaths.accounts.passwordReset}
                    element={<PasswordReset/>}
                />
                <Route
                    path={pagesPaths.accounts.passwordResetConfirm}
                    element={<PasswordResetConfirm/>}
                />
                <Route
                    path={pagesPaths.accounts.profile}
                    element={<Profile/>}
                />
                <Route
                    path={pagesPaths.schedule.group}
                    element={<GroupSchedulePage/>}
                />
                <Route
                    path={pagesPaths.schedule.teacherSearch}
                    element={<TeacherSearch/>}
                />
                <Route
                    path={pagesPaths.schedule.teacher}
                    element={<TeacherSchedulePage/>}
                />
            </Routes>
        </BrowserRouter>
    );
};

export default AppRoutes;