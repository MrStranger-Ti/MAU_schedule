import React from 'react';
import AppRoutes from "./AppRoutes";
import AuthProvider from "./context/main/AuthProvider";
import NotificationProvider from "./context/main/NotificationProvider";

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
