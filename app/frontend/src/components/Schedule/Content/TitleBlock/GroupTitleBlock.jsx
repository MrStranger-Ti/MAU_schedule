import React, {useContext} from 'react';
import {AuthContext} from "../../../../context/main/AuthProvider";
import Select from "../../../UI/Form/Select";
import LoadingButton from "../../../UI/Button/LoadingButton";
import Form from "../../../UI/Form/Form";
import {ScheduleContext} from "../../../../context/schedule/ScheduleProvider";
import {PeriodsContext} from "../../../../context/schedule/PeriodsProvider";

const TitleBlock = () => {
    const {userData} = useContext(AuthContext);
    const {fetchSchedule, isScheduleLoading, setIsScheduleLoading} = useContext(ScheduleContext);
    const {periods, currentPeriodValue, setCurrentPeriodValue} = useContext(PeriodsContext);

    const onSubmit = async (e) => {
        setIsScheduleLoading(true);

        e.preventDefault();
        await fetchSchedule(
            currentPeriodValue ? periods[currentPeriodValue].name : null
        );

        setIsScheduleLoading(false);
    }

    return (
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
    );
};

export default TitleBlock;