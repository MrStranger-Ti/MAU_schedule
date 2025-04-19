import BaseService from "./base";
import axios from "axios";
import config from "../config";

const url = `https://${config.API_HOST}/api/schedule/institutes/`

export default class instituteService extends BaseService {
    async getAll() {
        return await this.getResponse(() =>
            axios.get(url)
        )
    }

    async getById(id) {
        return await this.getResponse(() =>
            axios.get(`${url}${id}/`)
        )
    }
}