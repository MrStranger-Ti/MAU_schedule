import React, {useContext, useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import {Link} from "react-router-dom";
import Form from "../../../components/UI/Form/Form";
import InputErrors from "../../../components/UI/Form/InputErrors";
import Input from "../../../components/UI/Form/Input";
import {pagesPaths} from "../../../config";
import AuthService from "../../../services/auth";
import {LoadingContext} from "../../../context/base";
import BearFace from "../../../assets/images/logo/bear_face.png";

const PasswordReset = () => {
    const {setIsLoading} = useContext(LoadingContext);
    const [isSuccessEmailSent, setIsSuccessEmailSent] = useState(false);
    const [formData, setFormData] = useState({email: ""});
    const [formErrors, setFormErrors] = useState({});


    const onSubmit = async (e) => {
        e.preventDefault();

        setIsLoading(true);

        const service = new AuthService();
        const {success, data} = await service.passwordReset(formData);
        if (success) {
            setIsSuccessEmailSent(true);
        } else {
            setFormErrors(data);
        }

        setIsLoading(false);
    }

    return (
        <BaseAuth>
            <Helmet>
                <title>Восстановление пароля</title>
            </Helmet>
            {!isSuccessEmailSent
                ?
                <React.Fragment>
                    <h1 className="auth__title">Восстановление пароля</h1>
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
                        <button className="btn auth__btn" type="submit">Отправить</button>
                    </Form>
                    <Link className="link dark-link" to={pagesPaths.accounts.login}>Войти</Link>
                </React.Fragment>
                :
                <React.Fragment>
                    <img className="main-logo" src={BearFace} alt="логотип лицо медведя"/>
                    <p className="auth__descr">Письмо со ссылкой на сброс пароля успешно отправлено</p>
                    <Link className="btn auth__btn" to={pagesPaths.accounts.login}>Войти</Link>
                </React.Fragment>
            }
        </BaseAuth>
    );
};

export default PasswordReset;