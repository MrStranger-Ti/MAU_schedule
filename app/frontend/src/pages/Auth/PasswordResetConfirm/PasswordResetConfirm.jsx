import React, {useContext, useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import {LoadingContext} from "../../../context/base";
import Form from "../../../components/UI/Form/Form";
import AuthService from "../../../services/auth";
import {Link, useParams} from "react-router-dom";
import FormErrors from "../../../components/UI/Form/FormErrors";
import Input from "../../../components/UI/Form/Input";
import InputErrors from "../../../components/UI/Form/InputErrors";
import BearFace from "../../../assets/images/logo/bear_face.png";
import {pagesPaths} from "../../../config";

const PasswordResetConfirm = () => {
    const {uidb64, token} = useParams();

    const {setIsLoading} = useContext(LoadingContext);
    const [isSuccessPasswordChanged, setIsSuccessPasswordChanged] = useState(false);
    const [formData, setFormData] = useState({password1: "", password2: ""});
    const [formErrors, setFormErrors] = useState({});

    const onSubmit = async (e) => {
        e.preventDefault();

        setIsLoading(true);

        const service = new AuthService();
        const {success, data} = await service.passwordResetConfirm({uidb64, token}, formData);
        if (success) {
            setIsSuccessPasswordChanged(true);
        } else {
            setFormErrors(data);
            setFormData({password1: "", password2: ""})
        }

        setIsLoading(false);
    }

    return (
        <BaseAuth>
            <Helmet>
                <title>Изменение пароля</title>
            </Helmet>
            {!isSuccessPasswordChanged
                ?
                <React.Fragment>
                    <h1 className="auth__title">Изменение пароля</h1>
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
                        <button className="btn" type="submit">Изменить пароль</button>
                    </Form>
                    <Link className="link dark-link" to={pagesPaths.accounts.login}>Войти</Link>
                </React.Fragment>
                :
                <React.Fragment>
                    <img className="main-logo" src={BearFace} alt="логотип лицо медведя"/>
                    <p className="auth__descr">Пароль успешно изменен</p>
                    <Link className="btn auth__btn" to={pagesPaths.accounts.login}>Войти</Link>
                </React.Fragment>
            }
        </BaseAuth>
    );
};

export default PasswordResetConfirm;