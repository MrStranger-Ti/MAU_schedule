import React, {useContext, useState} from "react";
import Form from "../../components/UI/Form/Form";
import FormErrors from "../../components/UI/Form/FormErrors";
import Input from "../../components/UI/Form/Input";
import InputErrors from "../../components/UI/Form/InputErrors";
import userService from "../../services/user";
import InstituteService from "../../services/institute";
import {Helmet} from "react-helmet";
import Select from "../../components/UI/Form/Select";
import {AuthContext} from "../../context/AuthProvider";
import LoadingButton from "../../components/UI/Button/LoadingButton";

const ProfileForm = ({
                         setUpdating,
                         isBtnLoading,
                         setIsBtnLoading,
                         institutes
                     }) => {
    const {userData, setUserData} = useContext(AuthContext);

    const baseFromData = {
        full_name: userData.full_name,
        course: userData.course,
        group: userData.group,
        institute: userData.institute.id || "0"
    }
    const [formData, setFormData] = useState(baseFromData);
    const [formErrors, setFormErrors] = useState({});

    const onSubmit = async (e) => {
        e.preventDefault();

        if (formData === baseFromData) {
            setUpdating(false);
            return;
        }

        setIsBtnLoading(true);

        const updateResponse = await new userService().updateData(formData);

        if (updateResponse.success) {
            const updatingData = {
                full_name: updateResponse.data.full_name,
                email: updateResponse.data.email,
                course: updateResponse.data.course,
                group: updateResponse.data.group,
            };
            const service = new InstituteService();
            const instituteResponse = await service.getById(updateResponse.data.institute);

            if (instituteResponse.success) Object.assign(updatingData, {
                institute: instituteResponse.data,
            });

            setUserData(updatingData);
            setUpdating(false);
        } else {
            setFormErrors(updateResponse.data);
        }

        setIsBtnLoading(false);
    }

    return (
        <React.Fragment>
            <Helmet>
                <title>Обновление профиля</title>
            </Helmet>
            <Form
                className="profile__form"
                onSubmit={onSubmit}
                formErrors={formErrors}
                id="profile-update"
            >
                <FormErrors/>
                <div className="row row-cols-md-2 g-1 g-md-3 justify-content-between inputs-block flex-wrap">
                    <InputErrors inputName="full_name"/>
                    <div className="col-md field-block">
                        <div className="form-floating">
                            <Input
                                className="form-control"
                                type="text"
                                name="full_name"
                                id="full_name"
                                placeholder="full_name"
                                onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                                value={formData.full_name}
                                required
                            />
                            <label htmlFor="full_name">ФИО</label>
                        </div>
                    </div>
                    <InputErrors inputName="course"/>
                    <div className="col-md field-block">
                        <div className="form-floating">
                            <Input
                                className="form-control"
                                type="number"
                                name="course"
                                id="course"
                                placeholder="course"
                                onChange={(e) => setFormData({...formData, course: e.target.value})}
                                value={formData.course}
                                required
                            />
                            <label htmlFor="course">Курс</label>
                        </div>
                    </div>
                    <InputErrors inputName="group"/>
                    <div className="col-md field-block">
                        <div className="form-floating">
                            <Input
                                className="form-control"
                                type="text"
                                name="group"
                                id="group"
                                placeholder="group"
                                onChange={(e) => setFormData({...formData, group: e.target.value})}
                                value={formData.group}
                                required
                            />
                            <label htmlFor="group">Группа</label>
                        </div>
                    </div>
                    <InputErrors inputName="institute"/>
                    <div className="col-md field-block">
                        <div className="form-floating">
                            <Select
                                className="form-control form-select"
                                onChange={(e) => setFormData({...formData, institute: e.target.value})}
                                name="institute"
                                value={formData.institute}
                                options={institutes}
                                firstOption="Выберите институт"
                                type="text"
                                id="institute"
                                placeholder="institute"
                                required
                            />
                            <label htmlFor="full_name">Институт</label>
                        </div>
                    </div>
                </div>
            </Form>
            <div className="profile__btn-block">
                <LoadingButton
                    isLoading={isBtnLoading}
                    className="btn"
                    type="submit"
                    form="profile-update"
                >
                    Обновить
                </LoadingButton>
            </div>
        </React.Fragment>
    );
};

export default ProfileForm;