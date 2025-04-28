import React, {useState} from "react";
import BaseProfile from "./BaseProfile";
import ProfileForm from "./ProfileForm";
import DisplayProfile from "./DisplayProfile";
import instituteService from "../../services/institute";

const Profile = () => {
    const [isUpdating, setIsUpdating] = useState(false);
    const [isBtnLoading, setIsBtnLoading] = useState(false);
    const [institutes, setInstitutes] = useState([]);

    const loadUpdate = () => {
        const getInstitutes = async () => {
            setIsBtnLoading(true);

            const {success, data} = await new instituteService().service.getAll();
            if (success) setInstitutes(data);

            setIsBtnLoading(false);
            setIsUpdating(true);
        }

        getInstitutes();
    }

    return (
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
    );
};

export default Profile;