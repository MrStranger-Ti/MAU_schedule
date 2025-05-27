import React, {useState} from "react";
import FormErrors from "../../../components/UI/Form/FormErrors";
import InputErrors from "../../../components/UI/Form/InputErrors";
import Input from "../../../components/UI/Form/Input";
import Form from "../../../components/UI/Form/Form";
import {useNavigate} from "react-router-dom";
import AuthService from "../../../services/auth";
import LoadingButton from "../../../components/UI/Button/LoadingButton";
import {pagesPaths} from "../../../AppRoutes";

const LoginForm = () => {
    const [formData, setFormData] = useState({email: "", password: ""});
    const [formErrors, setFormErrors] = useState({});
    const [isBtnLoading, setIsBtnLoading] = useState(false);
    const navigate = useNavigate();

    const onSubmit = async (e) => {
        e.preventDefault();

        setIsBtnLoading(true);

        const {success, data} = await new AuthService().setToken(formData);
        if (success) {
            navigate(pagesPaths.schedule.group);
        } else {
            setFormErrors(data);
            setFormData({...formData, password: ""});
        }

        setIsBtnLoading(false);
    }

    return (
        <Form
            className="auth__form flex"
            onSubmit={onSubmit}
            formErrors={formErrors}
            setFormErrors={setFormErrors}
        >
            <div className="inputs-block flex">
                <FormErrors/>
                <div className="field-block">
                    <InputErrors inputName="email"/>
                    <div className="form-floating">
                        <Input
                            className="form-control"
                            value={formData.email}
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                            required
                            placeholder="example@mauniver.ru"
                            type="email"
                            id="floatingEmail"
                            name="email"
                        />
                        <label htmlFor="floatingEmail">Email</label>
                    </div>
                </div>
                <div className="field-block">
                    <InputErrors inputName="password"/>
                    <div className="form-floating">
                        <Input
                            className="form-control"
                            value={formData.password}
                            onChange={(e) => setFormData({...formData, password: e.target.value})}
                            required
                            placeholder="пароль"
                            type="password"
                            id="floatingPassword"
                            name="password"
                        />
                        <label htmlFor="floatingPassword">Пароль</label>
                    </div>
                </div>
            </div>
            <LoadingButton
                isLoading={isBtnLoading}
                className="btn"
                type="submit"
            >
                Войти
            </LoadingButton>
        </Form>
    );
};

export default LoginForm;