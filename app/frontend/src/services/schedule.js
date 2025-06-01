import BaseService from "./base";
import axios from "axios";
import {config} from "../config";

export default class ScheduleService extends BaseService {
    async getPeriods() {
        return await this.getResponse(() =>
            axios.get(`https://${config.API_HOST}/api/schedule/periods/`, {
                withCredentials: true
            })
        );
    }

    async getGroupSchedule(period) {
        return await this.getResponse(() =>
            axios.get(`https://${config.API_HOST}/api/schedule/group/`, {
                withCredentials: true,
                params: {period}
            })
        );
    }

    async getTeacherKeys(query) {
        return await this.getResponse(() =>
            axios.get(`https://${config.API_HOST}/api/schedule/teachers-keys/`, {
                withCredentials: true,
                params: {name: query}
            })
        );
    }

    async getTeacherSchedule(period, teacherKey) {
        return await this.getResponse(() =>
            axios.get(`https://${config.API_HOST}/api/schedule/teacher/${teacherKey}/`, {
                withCredentials: true,
                params: {period}
            })
        );
    }
}