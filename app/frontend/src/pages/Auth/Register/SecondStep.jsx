import React from "react";
import FormErrors from "../../../components/UI/Form/FormErrors";
import InputErrors from "../../../components/UI/Form/InputErrors";
import Input from "../../../components/UI/Form/Input";
import Select from "../../../components/UI/Form/Select";
import ButtonSpinner from "../../../components/Spinner/ButtonSpinner";

const SecondStep = ({setStep, formData, setFormData, institutes, isBtnLoading}) => {
    return (
        <div className="auth__step-2 flex">
            <div className="inputs-block flex">
                <FormErrors/>
                <div className="auth__field-block">
                    <InputErrors inputName="course"/>
                    <div className="form-floating">
                        <Input
                            className="form-control"
                            onChange={(e) => setFormData({...formData, course: e.target.value})}
                            name="course"
                            value={formData.course}
                            id="floatingCourse"
                            placeholder="course"
                            type="number"
                            required
                        />
                        <label htmlFor="floatingCourse">Курс</label>
                    </div>
                </div>
                <div className="auth__field-block">
                    <InputErrors inputName="institute"/>
                    <div className="form-floating">
                        <Select
                            className="form-control form-select"
                            onChange={(e) => setFormData({...formData, institute: e.target.value})}
                            name="institute"
                            value={formData.institute}
                            options={institutes}
                            firstOption="Выберите институт"
                            id="floatingInstitute"
                            placeholder="institute"
                            type="institute"
                            required
                        />
                        <label htmlFor="floatingInstitute">Институт</label>
                    </div>
                </div>
                <div className="auth__field-block">
                    <InputErrors inputName="group"/>
                    <div className="form-floating">
                        <Input
                            className="form-control"
                            onChange={(e) => setFormData({...formData, group: e.target.value})}
                            name="group"
                            value={formData.group}
                            id="floatingGroup"
                            placeholder="group"
                            type="group"
                            required
                        />
                        <label htmlFor="floatingGroup">Группа</label>
                    </div>
                </div>
            </div>
            <div className="auth__btns-block flex">
                <button
                    className="btn auth__btn"
                    type="button"
                    onClick={() => setStep(1)}
                >
                    Предыдущий шаг
                </button>
                <button
                    className="btn auth__btn"
                    type="submit"
                    disabled={isBtnLoading && true}
                >
                    {isBtnLoading && <ButtonSpinner/>}
                    Зарегистрироваться
                </button>
            </div>
        </div>
    );
};

export default SecondStep;