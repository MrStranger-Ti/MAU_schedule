import React, {useContext} from "react";
import {ScheduleContext} from "../../../../context/schedule/ScheduleProvider";
import {PeriodsContext} from "../../../../context/schedule/PeriodsProvider";
import Form from "../../../UI/Form/Form";
import Select from "../../../UI/Form/Select";
import LoadingButton from "../../../UI/Button/LoadingButton";

const TitleForm = () => {
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
    );
};

export default TitleForm;