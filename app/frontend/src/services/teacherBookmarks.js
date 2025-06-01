import BaseService from "./base";
import axios from "axios";
import {config} from "../config";

const url = `https://${config.API_HOST}/api/teacher-schedule-bookmarks/`;

export default class TeacherBookmarksService extends BaseService {
    async getAll() {
        return await this.getResponse(() =>
            axios.get(url, {
                withCredentials: true
            })
        );
    }

    async create({teacherName, teacherKey, userId}) {
        const data = JSON.stringify({
            teacher_name: teacherName,
            teacher_key: teacherKey,
            user: userId
        })
        return await this.getResponse(() =>
            axios.post(url, data, {
                headers: {
                    "Content-Type": "application/json"
                },
                withCredentials: true
            })
        )
    }

    async delete(id) {
        return await this.getResponse(() =>
            axios.delete(url + id + "/", {
                withCredentials: true
            })
        );
    }
}