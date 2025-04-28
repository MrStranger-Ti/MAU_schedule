import React, {useEffect, useRef, useState} from "react";
import BaseAuth from "../BaseAuth";
import {Helmet} from "react-helmet";
import Form from "../../../components/UI/Form/Form";
import FirstStep from "./FirstStep";
import SecondStep from "./SecondStep";
import instituteService from "../../../services/institute";
import {Link} from "react-router-dom";
import AuthService from "../../../services/auth";

const Register = () => {
    const [isSuccessRegister, setIsSuccessRegister] = useState(false);
    const [isFormLoading, setIsFormLoading] = useState(false);
    const baseFormData = {
        full_name: "",
        password: "",
        email: "",
        course: 1,
        institute: "",
        group: ""
    }
    const [formData, setFormData] = useState(baseFormData);
    const [formErrors, setFormErrors] = useState({});
    const [step, setStep] = useState(1);
    const [institutes, setInstitutes] = useState([]);

    const formRef = useRef(null);

    useEffect(() => {
        const getInstitutes = async () => {
            setIsFormLoading(true);

            const {success, data} = await new instituteService().getAll();
            if (success) setInstitutes(data);
            setIsFormLoading(false);
        }

        getInstitutes();
    }, []);

    const onSubmit = async (e) => {
        e.preventDefault();

        setIsFormLoading(true);

        const {success, data} = await new AuthService().register(formData);
        if (success) {
            setIsSuccessRegister(true);
        } else {
            setFormErrors(data);
            setFormData({...formData, password: ""});
            setStep(1);
        }

        setIsFormLoading(false);
    }

    return (
        <BaseAuth isLoading={isFormLoading}>
            <Helmet>
                <title>Регистрация</title>
            </Helmet>
            <h1 className="auth__title">Регистрация</h1>
            {!isSuccessRegister
                ?
                <React.Fragment>
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
                                setStep={setStep}
                                formData={formData}
                                setFormData={setFormData}
                                formRef={formRef}
                            />
                            :
                            <SecondStep
                                setStep={setStep}
                                formData={formData}
                                setFormData={setFormData}
                                institutes={institutes}
                                onSubmit={onSubmit}
                            />
                        }
                    </Form>
                    <div className="auth__link-block">
                        <Link className="dark-link link" to="/accounts/login/">Войти</Link>
                    </div>
                </React.Fragment>
                :
                <React.Fragment>
                    <p className="auth__descr">
                        Письмо отправлено. Перейдите по ссылке в письме, чтобы подтвердить почту.
                    </p>
                    <Link className="btn" to="/accounts/login/">Войти</Link>
                </React.Fragment>
            }
        </BaseAuth>
    );
};

export default Register;