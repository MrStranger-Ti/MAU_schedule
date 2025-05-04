import BaseService from "./base";
import axios from "axios";
import {config} from "../config";

const url = `https://${config.API_HOST}/api/me/`

export default class userService extends BaseService {
    async getUserData() {
        return await this.getResponse(() =>
            axios.get(url, {
                withCredentials: true
            })
        )
    }

    async updateData({full_name, course, institute, group}) {
        const data = JSON.stringify({full_name, course, institute, group})
        return await this.getResponse(() =>
            axios.put(url, data, {
                headers: {
                    "Content-Type": "application/json"
                },
                withCredentials: true
            })
        )
    }
}