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
import Auth from "./components/Auth/Auth";

const Routes = () => {
    return (
        <BrowserRouter>
            <R>
                <Route
                    path={pagesPaths.index}
                    element={
                        <Auth redirectAuthUser={true}>
                            <IndexPage/>
                        </Auth>
                    }
                />
                <Route
                    path={pagesPaths.accounts.login}
                    element={
                        <Auth redirectAuthUser={true}>
                            <Login/>
                        </Auth>
                    }
                />
                <Route
                    path={pagesPaths.accounts.register}
                    element={
                        <Auth stopLoading={false} redirectAuthUser={true}>
                            <Register/>
                        </Auth>
                    }
                />
                <Route
                    path={pagesPaths.accounts.registerConfirm}
                    element={
                        <Auth redirectAuthUser={true}>
                            <RegisterConfirm/>
                        </Auth>
                    }
                />
                <Route
                    path={pagesPaths.accounts.passwordReset}
                    element={
                        <Auth redirectAuthUser={true}>
                            <PasswordReset/>
                        </Auth>
                    }
                />
                <Route
                    path={pagesPaths.accounts.passwordResetConfirm}
                    element={
                        <Auth redirectAuthUser={true}>
                            <PasswordResetConfirm/>
                        </Auth>
                    }
                />
                <Route
                    path={pagesPaths.accounts.profile}
                    element={
                        <Auth protect={true}>
                            <Profile/>
                        </Auth>
                    }
                />
                <Route
                    path={pagesPaths.schedule.group}
                    element={
                        <Auth stopLoading={false} protect={true}>
                            <Group/>
                        </Auth>
                    }
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