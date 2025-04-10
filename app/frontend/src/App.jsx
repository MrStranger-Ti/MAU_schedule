import React, {useState} from 'react';
import Routes from "./routes";
import {AuthContext, LoadingContext} from "./context/auth";

function App() {
    const [isAuth, setIsAuth] = useState(false);
    const [isPageLoading, setIsPageLoading] = useState(true);

    return (
        <AuthContext.Provider value={{isAuth, setIsAuth}}>
            <LoadingContext.Provider value={{isPageLoading, setIsPageLoading}}>
                <div className="App">
                    <Routes/>
                </div>
            </LoadingContext.Provider>
        </AuthContext.Provider>
    );
}

export default App;
