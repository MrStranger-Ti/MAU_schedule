import {useEffect, useState} from "react";
import {useLocation} from "react-router-dom";

export const useChangeLocation = (callback) => {
    const location = useLocation();
    const [currentLocation, setCurrentLocation] = useState(location.pathname);

    useEffect(() => {
        if (location.pathname !== currentLocation) {
            callback();
            setCurrentLocation(location.pathname);
        }
    }, [location]);
}