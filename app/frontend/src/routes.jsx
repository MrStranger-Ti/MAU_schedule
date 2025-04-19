import React from "react";
import {BrowserRouter, Routes as R, Route} from "react-router-dom";
import IndexPage from "./pages/IndexPage";
import AuthRoute from "./components/Routes/AuthRoute";
import Profile from "./pages/Profile/Profile";
import Login from "./pages/Auth/Login";

const Routes = () => {
    return (
        <BrowserRouter>
            <R>
                <Route path="/" element={<IndexPage/>}/>
                <Route path="/accounts/login/" element={
                    <AuthRoute>
                        <Login/>
                    </AuthRoute>
                }/>
                <Route path="/accounts/register/" element=""/>
                <Route path="/accounts/profile/" element={
                    <AuthRoute>
                        <Profile/>
                    </AuthRoute>
                }
                />
                <Route path="/schedule/group/" element=""/>
                <Route path="/schedule/teacher-search/" element=""/>
            </R>
        </BrowserRouter>
    );
};

export default Routes;