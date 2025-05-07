import React, {useContext, useRef, useState} from "react";
import FirstStep from "./FirstStep";
import SecondStep from "./SecondStep";
import Form from "../../../components/UI/Form/Form";
import AuthService from "../../../services/auth";
import {LoadingContext} from "../../../context/base";

const RegisterForm = ({institutes, setIsSuccessRegister}) => {
    const [formData, setFormData] = useState({
        full_name: "",
        password: "",
        email: "",
        course: 1,
        institute: "",
        group: ""
    });
    const [formErrors, setFormErrors] = useState({});
    const [step, setStep] = useState(1);
    const [isBtnLoading, setIsBtnLoading] = useState(false);
    const formRef = useRef(null);

    const onSubmit = async (e) => {
        e.preventDefault();

        setIsBtnLoading(true);

        const service = new AuthService();
        const {success, data} = await service.register(formData);
        if (success) {
            setIsSuccessRegister(true);
        } else {
            setFormErrors(data);
            setFormData({...formData, password: ""});
            setStep(1);
        }

        setIsBtnLoading(false);
    }

    return (
        <Form
            ref={formRef}
            className="auth__form flex"
            formErrors={formErrors}
            setFormErrors={setFormErrors}
            onSubmit={onSubmit}
        >
            <h2 className="auth__step-title">Шаг&nbsp;<span>{step}</span>/2</h2>
            {step === 1
                ?
                <FirstStep
                    formRef={formRef}
                    setStep={setStep}
                    formData={formData}
                    setFormData={setFormData}
                />
                :
                <SecondStep
                    setStep={setStep}
                    formData={formData}
                    setFormData={setFormData}
                    institutes={institutes}
                    isBtnLoading={isBtnLoading}
                    onSubmit={onSubmit}
                />
            }
        </Form>
    );
};

export default RegisterForm;