import React, {useContext} from "react";
import Form from "../../../../components/UI/Form/Form";
import Select from "../../../../components/UI/Form/Select";
import ButtonSpinner from "../../../../components/Spinner/ButtonSpinner";
import Spinner from "../../../../components/Spinner/Spinner";
import {UserContext} from "../../../../context/auth";
import ScheduleTables from "./ScheduleTables";

const ScheduleContent = ({
                             fetchSchedule,
                             isScheduleLoading,
                             schedule,
                             periods,
                             currentPeriodValue,
                             setCurrentPeriodValue,
                         }) => {
    const {userData} = useContext(UserContext);

    const onSubmit = async (e) => {
        e.preventDefault();
        await fetchSchedule();
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
                    />
                    <button className="btn" type="submit" disabled={isScheduleLoading && true}>
                        {isScheduleLoading && <ButtonSpinner/>}
                        Найти
                    </button>
                </Form>
            </div>
            {isScheduleLoading
                ?
                <Spinner/>
                :
                <ScheduleTables schedule={schedule}/>
            }
        </div>
    );
};

export default ScheduleContent;