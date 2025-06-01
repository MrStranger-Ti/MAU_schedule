import React, {useContext} from "react";
import Form from "../../../UI/Form/Form";
import Select from "../../../UI/Form/Select/Select";
import LoadingButton from "../../../UI/Buttons/LoadingButton/LoadingButton";
import {ScheduleContext} from "../../../../context/schedule/ScheduleProvider";
import {PeriodsContext} from "../../../../context/schedule/PeriodsProvider";

const PeriodForm = () => {
    const {fetchSchedule, isScheduleLoading, setIsScheduleLoading} = useContext(ScheduleContext);
    const {periods, currentPeriodValue, setCurrentPeriodValue} = useContext(PeriodsContext);

    const handleOnSubmit = async (e) => {
        e.preventDefault();

        setIsScheduleLoading(true);

        await fetchSchedule(
            currentPeriodValue ? periods[currentPeriodValue].name : null
        );

        setIsScheduleLoading(false);
    }

    return (
        <Form
            className="schedule__form schedule__period-form flex"
            onSubmit={handleOnSubmit}
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

export default PeriodForm;