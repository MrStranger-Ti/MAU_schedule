import React, {useContext, useState} from "react";
import FormErrors from "../../../components/UI/Form/FormErrors";
import InputErrors from "../../../components/UI/Form/InputErrors";
import Input from "../../../components/UI/Form/Input";
import Form from "../../../components/UI/Form/Form";
import AuthService from "../../../services/auth";
import {useNavigate, useParams} from "react-router-dom";
import LoadingButton from "../../../components/UI/Buttons/LoadingButton/LoadingButton";
import {NotificationContext} from "../../../context/main/NotificationProvider";

import {pagesPaths} from "../../../AppRoutes";

const PasswordResetConfirmForm = () => {
    const {showNotification} = useContext(NotificationContext);
    const {uidb64, token} = useParams();
    const [formData, setFormData] = useState({password1: "", password2: ""});
    const [formErrors, setFormErrors] = useState({});
    const [isBtnLoading, setIsBtnLoading] = useState(false);
    const navigate = useNavigate();

    const onSubmit = async (e) => {
        e.preventDefault();

        setIsBtnLoading(true);

        const service = new AuthService();
        const {success, data} = await service.passwordResetConfirm({uidb64, token}, formData);
        if (success) {
            showNotification("Пароль успешно изменен");
            navigate(pagesPaths.accounts.login);
        } else {
            if (typeof data === "object" && Object.keys(data).length > 0) {
                setFormErrors(data);
                setFormData({password1: "", password2: ""});
                setIsBtnLoading(false);
            } else {
                showNotification("Не удалось изменить пароль");
                navigate(pagesPaths.accounts.login);
            }
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
                <FormErrors/>
                <div className="field-block">
                    <div className="form-floating">
                        <InputErrors inputName="password1"/>
                        <Input
                            className="form-control"
                            onChange={(e) => setFormData({...formData, password1: e.target.value})}
                            name="password1"
                            value={formData.password1}
                            placeholder="password1"
                            id="floatingPassword1"
                            type="password"
                            required
                        />
                        <label htmlFor="floatingPassword1">Новый пароль</label>
                    </div>
                </div>
                <div className="auth__field-block">
                    <div className="form-floating">
                        <InputErrors inputName="password2"/>
                        <Input
                            className="form-control"
                            onChange={(e) => setFormData({...formData, password2: e.target.value})}
                            name="password2"
                            value={formData.password2}
                            placeholder="password2"
                            id="floatingPassword2"
                            type="password"
                            required
                        />
                        <label htmlFor="floatingPassword2">Подтверждение нового пароля</label>
                    </div>
                </div>
            </div>
            <LoadingButton
                isLoading={isBtnLoading}
                className="btn"
                type="submit"
            >
                Изменить пароль
            </LoadingButton>
        </Form>
    );
};

export default PasswordResetConfirmForm;