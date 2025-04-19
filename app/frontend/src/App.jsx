import React, {useState} from 'react';
import Routes from "./routes";
import {AuthContext} from "./context/auth";

function App() {
    const [isAuth, setIsAuth] = useState(false);
    const [isCheckAuth, setIsCheckAuth] = useState(false);

    return (
        <AuthContext.Provider value={{isAuth, setIsAuth, isCheckAuth, setIsCheckAuth}}>
            <div className="App">
                <Routes/>
            </div>
        </AuthContext.Provider>
    );
}

export default App;
