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

    async delete(id) {
        return await this.getResponse(() =>
            axios.delete(url + id + "/", {
                withCredentials: true
            })
        );
    }
}