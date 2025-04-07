import React, {useEffect, useState} from 'react';
import Routes from "./routes";
import {AuthContext} from "./context/auth";
import AuthService from "./services/auth";
import {Navigate} from "react-router-dom";

function App() {
    const [isAuth, setIsAuth] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    return (
        <AuthContext.Provider value={{isAuth, setIsAuth, isLoading, setIsLoading}}>
            <div className="App">
                <Routes/>
            </div>
        </AuthContext.Provider>
    );
}

export default App;
