import React from "react";
import {BrowserRouter, Routes as R, Route} from "react-router-dom";
import IndexPage from "./pages/IndexPage";
import Profile from "./pages/Profile/Profile";
import Login from "./pages/Auth/Login/Login";
import Register from "./pages/Auth/Register/Register";
import RegisterConfirm from "./pages/Auth/RegisterConfirm/RegisterConfirm";
import PasswordReset from "./pages/Auth/PasswordReset/PasswordReset";
import {pagesPaths} from "./config";
import PasswordResetConfirm from "./pages/Auth/PasswordResetConfirm/PasswordResetConfirm";
import Group from "./pages/Schedule/Group/Group";

const Routes = () => {
    return (
        <BrowserRouter>
            <R>
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
                    element={<Group/>}
                />
                <Route
                    path={pagesPaths.schedule.teacherSearch}
                    element=""
                />
                <Route
                    path={pagesPaths.schedule.teacher}
                    element=""
                />
            </R>
        </BrowserRouter>
    );
};

export default Routes;