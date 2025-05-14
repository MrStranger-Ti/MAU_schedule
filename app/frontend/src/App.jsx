import React from 'react';
import AppRoutes from "./AppRoutes";
import AuthProvider from "./context/AuthProvider";

function App() {
    return (
        <AuthProvider>
            <div className="App">
                <AppRoutes/>
            </div>
        </AuthProvider>
    );
}

export default App;
