import React, {useContext, useState} from "react";
import FormErrors from "../../components/UI/Form/FormErrors";
import Form from "../../components/UI/Form/Form";
import Input from "../../components/UI/Form/Input";
import AuthService from "../../services/auth";
import {AuthContext} from "../../context/auth";
import InputErrors from "../../components/UI/Form/InputErrors";

const LoginForm = () => {
    const {setIsAuth} = useContext(AuthContext);
    const [formData, setFormData] = useState({email: "", password: ""});

    const request = async ({...params}) => new AuthService().login(params);
    const successful = () => setIsAuth(true);
    const unsuccessful = () => setFormData({...formData, password: ""});

    return (
        <Form
            className="auth__form flex"
            formData={formData}
            request={request}
            successful={successful}
            unsuccessful={unsuccessful}
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
            <button className="btn" type="submit">Войти</button>
        </Form>
    );
};

export default LoginForm;