import React from "react";
import {BrowserRouter, Routes as R, Route} from "react-router-dom";
import IndexPage from "./pages/IndexPage";
import ProtectedRoute from "./components/Auth/ProtectedRoute";
import Profile from "./pages/Profile";
import Login from "./pages/Login";

const Routes = () => {
    return (
        <div>
            <BrowserRouter>
                <R>
                    <Route path="/" element={<IndexPage/>}/>
                    <Route path="/accounts/login/" element={<Login/>}/>
                    <Route path="/accounts/register/" element=""/>
                    <Route
                        path="/accounts/profile/"
                        element={
                            <ProtectedRoute>
                                <Profile/>
                            </ProtectedRoute>
                        }
                    />
                    <Route path="/schedule/group/" element=""/>
                    <Route path="/schedule/teacher-search/" element=""/>
                </R>
            </BrowserRouter>
        </div>
    );
};

export default Routes;