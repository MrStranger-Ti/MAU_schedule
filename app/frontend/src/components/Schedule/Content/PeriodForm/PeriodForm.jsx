import React, {useContext, useState} from "react";
import Form from "../../../UI/Form/Form";
import Select from "../../../UI/Form/Select/Select";
import LoadingButton from "../../../UI/Buttons/LoadingButton/LoadingButton";
import {ScheduleContext} from "../../../../context/schedule/ScheduleProvider";
import {PeriodsContext} from "../../../../context/schedule/PeriodsProvider";
import styles from "../../../../styles/pages/Schedule.module.css";

const PeriodForm = () => {
    const {fetchSchedule, isScheduleLoading, setIsScheduleLoading} = useContext(ScheduleContext);
    const {periods, currentPeriodValue, setCurrentPeriodValue} = useContext(PeriodsContext);
    const [isCurrentPeriodsChanged, setIsCurrentPeriodChanged] = useState(false);

    const handleOnSubmit = async (e) => {
        e.preventDefault();

        if (!isCurrentPeriodsChanged) return;

        setIsScheduleLoading(true);

        await fetchSchedule(
            currentPeriodValue ? periods[currentPeriodValue].name : null
        );

        setIsCurrentPeriodChanged(false);
        setIsScheduleLoading(false);
    }

    const handleOnChange = (e) => {
        setCurrentPeriodValue(e.target.value);
        setIsCurrentPeriodChanged(true);
    }

    return (
        <Form
            className={styles.form}
            onSubmit={handleOnSubmit}
        >
            <Select
                onChange={handleOnChange}
                name="period"
                value={currentPeriodValue}
                options={periods}
                firstOption="Выберите период"
                required
            />
            <LoadingButton
                className={styles.button}
                isLoading={isScheduleLoading}
                type="submit"
            >
                Найти
            </LoadingButton>
        </Form>
    );
};

export default PeriodForm;