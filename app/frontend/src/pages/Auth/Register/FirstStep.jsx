import React from "react";
import FormErrors from "../../../components/UI/Form/FormErrors";
import InputErrors from "../../../components/UI/Form/InputErrors";
import Input from "../../../components/UI/Form/Input";

const FirstStep = React.forwardRef(({setStep, formData, setFormData, formRef}) => {
    const switchStep = () => {
        if (formRef.current.reportValidity()) {
            setStep(2);
        }
    }

    return (
        <div className="auth__step-1 flex">
            <div className="inputs-block flex">
                <FormErrors/>
                <div className="auth__field-block">
                    <InputErrors inputName="full_name"/>
                    <div className="form-floating">
                        <Input
                            className="form-control"
                            onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                            name="full_name"
                            value={formData.full_name}
                            id="floatingFullName"
                            placeholder="full_name"
                            type="text"
                            required
                        />
                        <label htmlFor="floatingFullName">ФИО</label>
                    </div>
                </div>
                <div className="auth__field-block">
                    <InputErrors inputName="email"/>
                    <div className="form-floating">
                        <Input
                            className="form-control"
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                            name="email"
                            value={formData.email}
                            id="email"
                            placeholder="email"
                            type="email"
                            required
                        />
                        <label htmlFor="floatingEmail">Email</label>
                    </div>
                </div>
                <div className="auth__field-block">
                    <InputErrors inputName="password"/>
                    <div className="form-floating">
                        <Input
                            className="form-control"
                            onChange={(e) => setFormData({...formData, password: e.target.value})}
                            name="password"
                            value={formData.password}
                            id="floatingPassword"
                            placeholder="password"
                            type="password"
                            required
                        />
                        <label htmlFor="floatingPassword">Пароль</label>
                    </div>
                </div>
            </div>
            <div className="auth__btns-block flex">
                <button
                    className="btn auth__btn"
                    type="button"
                    onClick={switchStep}
                >
                    Следующий шаг
                </button>
            </div>
        </div>
    );
});

export default FirstStep;