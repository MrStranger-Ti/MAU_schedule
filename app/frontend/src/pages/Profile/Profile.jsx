import React, {useContext, useState} from "react";
import BaseProfile from "./BaseProfile";
import ProfileForm from "./ProfileForm";
import DisplayProfile from "./DisplayProfile";
import InstituteService from "../../services/institute";
import {useAuth} from "../../hooks/auth/useAuth";
import {LoadingContext} from "../../context/main/LoadingProvider";
import {NotificationContext} from "../../context/main/NotificationProvider";

const Profile = () => {
    const {showNotification} = useContext(NotificationContext);
    const [isLoading, setIsLoading] = useState(true);
    const [isUpdating, setIsUpdating] = useState(false);
    const [isBtnLoading, setIsBtnLoading] = useState(false);
    const [institutes, setInstitutes] = useState([]);

    useAuth(setIsLoading, {
        protect: true
    });

    const loadUpdate = () => {
        const getInstitutes = async () => {
            setIsBtnLoading(true);

            const {success, data} = await new InstituteService().getAll();
            if (success) {
                setInstitutes(data);
            } else {
                showNotification(data.detail, {error: true});
            }

            setIsBtnLoading(false);
            setIsUpdating(true);
        }

        getInstitutes();
    }

    return (
        <LoadingContext value={{isLoading, setIsLoading}}>
            <BaseProfile title={isUpdating ? "Обновление профиля" : "Профиль"}>
                {isUpdating
                    ?
                    <ProfileForm
                        setUpdating={setIsUpdating}
                        isBtnLoading={isBtnLoading}
                        setIsBtnLoading={setIsBtnLoading}
                        institutes={institutes}
                    />
                    :
                    <DisplayProfile
                        isBtnLoading={isBtnLoading}
                        loadUpdate={loadUpdate}
                    />
                }
            </BaseProfile>
        </LoadingContext>
    );
};

export default Profile;