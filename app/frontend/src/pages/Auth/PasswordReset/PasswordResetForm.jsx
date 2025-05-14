import React, {useContext, useState} from "react";
import InputErrors from "../../../components/UI/Form/InputErrors";
import Input from "../../../components/UI/Form/Input";
import Form from "../../../components/UI/Form/Form";
import AuthService from "../../../services/auth";
import {LoadingContext} from "../../../context/LoadingProvider";

const PasswordResetForm = ({setIsSuccessEmailSent}) => {
    const {setIsLoading} = useContext(LoadingContext);
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
    );
};

export default PasswordResetForm;