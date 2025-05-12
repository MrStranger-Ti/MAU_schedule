import React, {useState} from 'react';
import Routes from "./routes";
import {LoadingContext} from "./context/base";
import {UserContext} from "./context/auth";

function App() {
    const [isLoading, setIsLoading] = useState(true);
    const [userData, setUserData] = useState({});

    return (
        <LoadingContext.Provider value={{isLoading, setIsLoading}}>
            <UserContext.Provider value={{userData, setUserData}}>
                <div className="App">
                    <Routes/>
                </div>
            </UserContext.Provider>
        </LoadingContext.Provider>
    );
}

export default App;
