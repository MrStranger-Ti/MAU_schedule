import React, {useState} from "react";
import BaseProfile from "./BaseProfile";
import ProfileForm from "./ProfileForm";
import DisplayProfile from "./DisplayProfile";
import InstituteService from "../../services/institute";
import Auth from "../../components/Auth/Auth";

const Profile = () => {
    const [isUpdating, setIsUpdating] = useState(false);
    const [isBtnLoading, setIsBtnLoading] = useState(false);
    const [institutes, setInstitutes] = useState([]);

    const loadUpdate = () => {
        const getInstitutes = async () => {
            setIsBtnLoading(true);

            const {success, data} = await new InstituteService().getAll();
            if (success) setInstitutes(data);

            setIsBtnLoading(false);
            setIsUpdating(true);
        }

        getInstitutes();
    }

    return (
        <Auth protect={true}>
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
        </Auth>
    );
};

export default Profile;