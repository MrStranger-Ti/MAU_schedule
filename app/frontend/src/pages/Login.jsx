import React, {useContext} from "react";
import AuthService from "../services/auth";
import {AuthContext} from "../context/auth";
import {Navigate} from "react-router-dom";
import BaseAuth from "./BaseAuth";
import {Helmet} from "react-helmet";

const Login = () => {
    const {isAuth, setIsAuth, isLoading, setIsLoading} = useContext(AuthContext);

    const login = async (e) => {
        e.preventDefault();

        setIsLoading(true)
        const service = new AuthService()
        const {success, data, error} = await service.login(
            e.target.elements["email"].value,
            e.target.elements["password"].value
        );

        if (success) setIsAuth(true);
        setIsLoading(false);
    }

    if (isAuth) {
        return <Navigate to="/accounts/profile/"/>
    }

    return (
        <BaseAuth>
            <Helmet>
                <title>Вход</title>
            </Helmet>
            <h1 className="auth__title">Вход</h1>
            <form class="auth__form flex" onSubmit={login}>
                <div class="auth__inputs-block flex">
                    {% if form.non_field_errors %}
                    <ul class="errors-list">
                        {% for error in form.non_field_errors %}
                        <li class="auth__error">{{error}}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                    {% for field in form %}
                    <div class="auth__field-block">
                        {% if field.errors %}
                        <ul class="errors-list">
                            {% for error in field.errors %}
                            <li class="auth__error">{{error}}</li>
                            {% endfor %}
                        </ul>
                        {% endif %}
                        <div class="form-floating {% if field.errors %}error{% endif %}">
                            {{field}}
                            {{field.label_tag}}
                        </div>
                    </div>
                    {% endfor %}
                </div>
                <button class="btn auth__btn" type="submit">Войти</button>
            </form>
            <a class="dark-link link" href="{% url 'mau_auth:registration' %}">Регистрация</a>
            <a class="dark-link link" href="{% url 'mau_auth:password_reset_form' %}">Восстановить пароль</a>
        </BaseAuth>
    );
};

export default Login;