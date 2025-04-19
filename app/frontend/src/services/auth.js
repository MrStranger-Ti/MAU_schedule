import axios from "axios";
import config from "../config"
import BaseService from "./base";

export default class AuthService extends BaseService {
    async login({email, password}) {
        const data = JSON.stringify({email, password})
        return await this.getResponse(() =>
            axios.post(`https://${config.API_HOST}/api/token/set/`, data, {
                headers: {
                    "Content-Type": "application/json"
                },
                withCredentials: true
            })
        )
    }

    async logout() {
        return await this.getResponse(() =>
            axios.post(`https://${config.API_HOST}/api/token/delete/`, null, {
                withCredentials: true
            })
        )
    }
}