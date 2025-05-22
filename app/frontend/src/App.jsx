import React from 'react';
import AppRoutes from "./AppRoutes";
import AuthProvider from "./context/AuthProvider";
import NotificationProvider from "./context/NotificationProvider";

function App() {
    return (
        <AuthProvider>
            <NotificationProvider>
                <div className="App">
                    <AppRoutes/>
                </div>
            </NotificationProvider>
        </AuthProvider>
    );
}

export default App;
