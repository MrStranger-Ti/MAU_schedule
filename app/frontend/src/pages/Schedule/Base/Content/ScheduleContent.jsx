import React, {useContext} from "react";
import Form from "../../../../components/UI/Form/Form";
import Select from "../../../../components/UI/Form/Select";
import ButtonSpinner from "../../../../components/Spinner/ButtonSpinner";
import Spinner from "../../../../components/Spinner/Spinner";
import ScheduleTables from "./ScheduleTables";
import {AuthContext} from "../../../../context/AuthProvider";
import {ScheduleContext} from "../../../../context/ScheduleProvider";
import LoadingButton from "../../../../components/UI/Button/LoadingButton";

const ScheduleContent = () => {
    const {
        fetchSchedule,
        isScheduleLoading,
        setIsScheduleLoading,
        periods,
        currentPeriodValue,
        setCurrentPeriodValue
    } = useContext(ScheduleContext);
    const {userData} = useContext(AuthContext);

    const onSubmit = async (e) => {
        setIsScheduleLoading(true);

        e.preventDefault();
        await fetchSchedule();

        setIsScheduleLoading(false);
    }

    return (
        <div className="schedule__content">
            <div className="schedule__title-block flex">
                <h1 className="schedule__title title">{userData.group}</h1>
                <Form
                    className="schedule__form schedule__period-form flex"
                    onSubmit={onSubmit}
                >
                    <Select
                        className="form-select"
                        onChange={(e) => setCurrentPeriodValue(e.target.value)}
                        name="period"
                        value={currentPeriodValue}
                        options={periods}
                        firstOption="Выберите период"
                        required
                    />
                    <LoadingButton
                        isLoading={isScheduleLoading}
                        className="btn"
                        type="submit"
                    >
                        Найти
                    </LoadingButton>
                </Form>
            </div>
            {isScheduleLoading
                ?
                <Spinner/>
                :
                <ScheduleTables/>
            }
        </div>
    );
};

export default ScheduleContent;