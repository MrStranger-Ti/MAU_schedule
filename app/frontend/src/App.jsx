import React, {useState} from 'react';
import Routes from "./routes";
import {AuthContext} from "./context/auth";
import {LoadingContext} from "./context/base";

function App() {
    const [isAuth, setIsAuth] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    return (
        <AuthContext.Provider value={{isAuth, setIsAuth}}>
            <LoadingContext.Provider value={{isLoading, setIsLoading}}>
                <div className="App">
                    <Routes/>
                </div>
            </LoadingContext.Provider>
        </AuthContext.Provider>
    );
}

export default App;
