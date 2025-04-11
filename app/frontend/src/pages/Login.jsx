import React, {useContext, useEffect, useState} from "react";
import AuthService from "../services/auth";
import {AuthContext, LoadingContext} from "../context/auth";
import {Link, Navigate, useNavigate} from "react-router-dom";
import {Helmet} from "react-helmet";
import BaseAuth from "../components/BasePages/BaseAuth";
import Main from "../components/BasePages/Main";
import Input from "../components/UI/Input";
import Form from "../components/UI/Form"

const Login = () => {
    const {isAuth, setIsAuth} = useContext(AuthContext);

    const [formData, setFormData] = useState({email: "", password: ""});
    const [hasErrors, setHasErrors] = useState(false);

    const request = async ({...params}) => new AuthService().login(params);
    const successful = () => setIsAuth(true);
    const unsuccessful = () => setFormData({...formData, password: ""});

    return (
        <BaseAuth>
            <Helmet>
                <title>Вход</title>
            </Helmet>
            {isAuth
                ?
                <Navigate to="/accounts/profile/"/>
                :
                <React.Fragment>
                    <h1 className="auth__title">Вход</h1>
                    <Form
                        request={request}
                        successful={successful}
                        unsuccessful={unsuccessful}
                        formData={formData}
                        setFormData={setFormData}
                        hasErrors={hasErrors}
                        setHasErrors={setHasErrors}
                        classPrefix="auth"
                    >
                        <Input
                            hasErrors={hasErrors}
                            labelText="Email"
                            value={formData.email}
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                            required
                            placeholder="example@mauniver.ru"
                            type="email"
                            id="floatingEmail"
                            name="email"
                        />
                        <Input
                            hasErrors={hasErrors}
                            labelText="Пароль"
                            value={formData.password}
                            onChange={(e) => setFormData({...formData, password: e.target.value})}
                            required
                            placeholder="пароль"
                            type="password"
                            id="floatingPassword"
                            name="password"
                        />
                    </Form>
                    <Link className="dark-link link" to="#">Регистрация</Link>
                    <Link className="dark-link link" to="#">Восстановить пароль</Link>
                </React.Fragment>
            }
        </BaseAuth>
    );
};

export default Login;