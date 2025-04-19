import React, {useState} from "react";
import BaseProfile from "./BaseProfile";
import {Helmet} from "react-helmet";
import ProfileForm from "./ProfileForm";
import DisplayProfile from "./DisplayProfile";

const Profile = () => {
    const [updating, setUpdating] = useState(false);

    return (
        <BaseProfile title="Профиль">
            <Helmet>
                <title>Профиль</title>
            </Helmet>
            {updating
                ?
                <ProfileForm setUpdating={updating}/>
                :
                <DisplayProfile/>
            }
            <div className="profile__btn-block">
                <button
                    className="btn"
                    type="button"
                    onClick={() => setUpdating(!updating)}
                >{updating ? "Обновить" : "Редактировать"}</button>
            </div>
        </BaseProfile>
    );
};

export default Profile;