import BaseService from "./base";
import axios from "axios";
import config from "../config";

const url = `https://${config.API_HOST}/api/schedule/institutes/`

export default class instituteService extends BaseService {
    async getAll() {
        const response = await this.getResponse(() =>
            axios.get(url)
        );

        const formatedInstitutes = response.data.map(institute => ({
            name: institute.name,
            value: institute.id
        }));

        if (response.success) {
            return {success: response.success, data: formatedInstitutes};
        }

        return {success: response.success, data: response.data};
    }

    async getById(id) {
        return await this.getResponse(() =>
            axios.get(`${url}${id}/`)
        );
    }
}