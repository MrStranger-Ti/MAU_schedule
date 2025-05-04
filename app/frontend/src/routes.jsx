import React from "react";
import {BrowserRouter, Routes as R, Route} from "react-router-dom";
import IndexPage from "./pages/IndexPage";
import AuthRoute from "./components/Routes/AuthRoute";
import Profile from "./pages/Profile/Profile";
import Login from "./pages/Auth/Login/Login";
import Register from "./pages/Auth/Register/Register";
import RegisterConfirm from "./pages/Auth/RegisterConfirm/RegisterConfirm";
import LogoutRoute from "./components/Routes/LogoutRoute";
import PasswordReset from "./pages/Auth/PasswordReset/PasswordReset";
import {pagesPaths} from "./config";
import PasswordResetConfirm from "./pages/Auth/PasswordResetConfirm/PasswordResetConfirm";

const Routes = () => {
    return (
        <BrowserRouter>
            <R>
                <Route
                    path={pagesPaths.index}
                    element={<IndexPage/>}
                />
                <Route path={pagesPaths.accounts.login} element={
                    <LogoutRoute>
                        <Login/>
                    </LogoutRoute>
                }/>
                <Route
                    path={pagesPaths.accounts.register}
                    element={
                        <LogoutRoute>
                            <Register/>
                        </LogoutRoute>
                    }
                />
                <Route
                    path={pagesPaths.accounts.registerConfirm}
                    element={
                        <LogoutRoute>
                            <RegisterConfirm/>
                        </LogoutRoute>
                    }
                />
                <Route
                    path={pagesPaths.accounts.passwordReset}
                    element={
                        <LogoutRoute>
                            <PasswordReset/>
                        </LogoutRoute>
                    }
                />
                <Route
                    path={pagesPaths.accounts.passwordResetConfirm}
                    element={
                        <LogoutRoute>
                            <PasswordResetConfirm/>
                        </LogoutRoute>
                    }
                />
                <Route path={pagesPaths.accounts.profile} element={
                    <AuthRoute>
                        <Profile/>
                    </AuthRoute>
                }
                />
                <Route
                    path={pagesPaths.schedule.group}
                    element=""
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