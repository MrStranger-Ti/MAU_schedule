import React, {useState} from "react";
import BaseProfile from "./BaseProfile";
import ProfileForm from "./ProfileForm";
import DisplayProfile from "./DisplayProfile";

const Profile = () => {
    const [updating, setUpdating] = useState(false);

    return (
        <BaseProfile title="Профиль">
            {updating
                ?
                <ProfileForm setUpdating={updating}/>
                :
                <DisplayProfile/>
            }
            <div className="profile__btn-block">
                <button
                    className="btn"
                    type={updating ? "submit" : "button"}
                    onClick={() => setUpdating(!updating)}
                    form={updating ? "profile-update" : "false"}
                >{updating ? "Обновить" : "Редактировать"}</button>
            </div>
        </BaseProfile>
    );
};

export default Profile;