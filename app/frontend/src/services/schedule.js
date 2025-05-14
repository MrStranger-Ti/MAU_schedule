import BaseService from "./base";
import axios from "axios";
import {config} from "../config";

export default class ScheduleService extends BaseService {
    async getPeriods() {
        return await this.getResponse(() =>
            axios.get(`https://${config.API_HOST}/api/schedule/periods/`, {
                withCredentials: true
            })
        )
    }

    async getGroupSchedule(period) {
        return await this.getResponse(() =>
            axios.get(`https://${config.API_HOST}/api/schedule/group/`, {
                withCredentials: true,
                params: {period}
            })
        )
    }

    async getTeacherSchedule(period) {

    }
}