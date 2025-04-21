import React, {useContext, useState} from "react";
import FormErrors from "../../../components/UI/Form/FormErrors";
import Form from "../../../components/UI/Form/Form";
import Input from "../../../components/UI/Form/Input";
import AuthService from "../../../services/auth";
import {AuthContext} from "../../../context/auth";
import InputErrors from "../../../components/UI/Form/InputErrors";
import ButtonSpinner from "../../../components/Spinner/ButtonSpinner";

const LoginForm = () => {
    const {setIsAuth} = useContext(AuthContext);
    const [formData, setFormData] = useState({email: "", password: ""});
    const [formErrors, setFormErrors] = useState({});
    const [isBtnLoading, setIsBtnLoading] = useState(false);

    const onSubmit = async (e) => {
        e.preventDefault();

        setIsBtnLoading(true);

        const {success, data} = await new AuthService().login(formData);
        if (success) {
            setIsAuth(true);
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
            <button className="btn" type="submit" disabled={isBtnLoading && true}>
                {isBtnLoading && <ButtonSpinner/>}
                Войти
            </button>
        </Form>
    );
};

export default LoginForm;