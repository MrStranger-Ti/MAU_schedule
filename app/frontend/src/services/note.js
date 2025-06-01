import BaseService from "./base";
import axios from "axios";
import {config} from "../config";

const url = `https://${config.API_HOST}/api/notes/`;

export default class NoteService extends BaseService {
    async getAll() {
        return await this.getResponse(() =>
            axios.get(url, {
                withCredentials: true
            })
        )
    }

    async create({
        schedule_name,
        schedule_key,
        day,
        lesson_number,
        text,
        user
    }) {
        const data = JSON.stringify({
            schedule_name,
            schedule_key,
            day,
            lesson_number,
            text,
            user
        })
        return await this.getResponse(() =>
            axios.post(url, data, {
                headers: {
                    "Content-Type": "application/json",
                },
                withCredentials: true
            })
        )
    }

    async update(id, text) {
        const data = JSON.stringify({text})
        return await this.getResponse(() =>
            axios.patch(url + id + "/", data, {
                headers: {
                    "Content-Type": "application/json",
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
        )
    }
}