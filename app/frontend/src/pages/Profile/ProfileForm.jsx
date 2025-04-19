import React, {useContext, useEffect, useState} from "react";
import Form from "../../components/UI/Form/Form";
import FormErrors from "../../components/UI/Form/FormErrors";
import Input from "../../components/UI/Form/Input";
import InputErrors from "../../components/UI/Form/InputErrors";
import userService from "../../services/user";
import {UserContext} from "../../context/auth";
import instituteService from "../../services/institute";
import Spinner from "../../components/Spinner/Spinner";
import {Helmet} from "react-helmet";
import Select from "../../components/UI/Form/Select";

const ProfileForm = ({setUpdating}) => {
    const {userData} = useContext(UserContext);
    const [institutes, setInstitutes] = useState([]);
    const [isFormLoading, setIsFormLoading] = useState(false);
    const [formData, setFormData] = useState({...userData, institute: userData.institute.name});

    useEffect(() => {
        const getInstitutes = async () => {
            setIsFormLoading(true);
            const service = new instituteService();
            const {success, data} = await service.getAll();

            if (success) {
                setInstitutes(data.map(institute => ({
                    name: institute.name,
                    value: institute.id
                })));
            }

            setIsFormLoading(false);
        }

        getInstitutes();
    }, []);

    const request = async () => new userService().getUserData();
    const successful = () => setUpdating(false);

    return (
        <React.Fragment>
            <Helmet>
                <title>Обновление профиля</title>
            </Helmet>
            {isFormLoading
                ?
                <Spinner/>
                :
                <Form
                    className="profile__form"
                    formData={formData}
                    request={request}
                    successful={successful}
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
                                />
                                <label htmlFor="course">Курс</label>
                            </div>
                        </div>
                        <InputErrors inputName="grouop"/>
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
                                />
                                <label htmlFor="group">Группа</label>
                            </div>
                        </div>
                        <InputErrors inputName="institute"/>
                        <div className="col-md field-block">
                            <div className="form-floating">
                                <Select
                                    options={institutes}
                                    className="form-control"
                                    type="text"
                                    name="institute"
                                    id="institute"
                                    placeholder="institute"
                                    onChange={(e) => setFormData({...formData, institute: e.target.value})}
                                    value={formData.institute}
                                />
                                <label htmlFor="full_name">Институт</label>
                            </div>
                        </div>
                    </div>
                </Form>
            }
        </React.Fragment>
    );
};

export default ProfileForm;