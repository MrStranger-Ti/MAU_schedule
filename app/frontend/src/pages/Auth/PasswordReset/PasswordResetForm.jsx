import React, {useContext, useState} from "react";
import InputErrors from "../../../components/UI/Form/InputErrors";
import Input from "../../../components/UI/Form/Input";
import Form from "../../../components/UI/Form/Form";
import AuthService from "../../../services/auth";
import LoadingButton from "../../../components/UI/Buttons/LoadingButton/LoadingButton";
import {NotificationContext} from "../../../context/main/NotificationProvider";
import {useNavigate} from "react-router-dom";

import {pagesPaths} from "../../../AppRoutes";

const PasswordResetForm = () => {
    const {showNotification} = useContext(NotificationContext);
    const [formData, setFormData] = useState({email: ""});
    const [formErrors, setFormErrors] = useState({});
    const [isBtnLoading, setIsBtnLoading] = useState(false);
    const navigate = useNavigate();

    const onSubmit = async (e) => {
        e.preventDefault();

        setIsBtnLoading(true);

        const service = new AuthService();
        const {success, data} = await service.passwordReset(formData);
        if (success) {
            showNotification(`Письмо с подтверждение отправлено на ${formData.email}`);
            navigate(pagesPaths.accounts.login);
        } else {
            setFormErrors(data);
            setIsBtnLoading(false);
        }
    }

    return (
        <Form
            className="auth__form flex"
            formErrors={formErrors}
            setFormErrors={setFormErrors}
            onSubmit={onSubmit}
        >
            <div className="inputs-block flex">
                <div className="field-block">
                    <InputErrors inputName="email"/>
                    <div className="form-floating">
                        <Input
                            className="form-control"
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                            name="email"
                            value={formData.email}
                            id="floatingEmail"
                            placeholder="email"
                            type="email"
                            required
                        />
                        <label htmlFor="floatingEmail">Email</label>
                    </div>
                </div>
            </div>
            <LoadingButton
                isLoading={isBtnLoading}
                className="btn auth__btn"
                type="submit"
            >
                Отправить</LoadingButton>
        </Form>
    );
};

export default PasswordResetForm;