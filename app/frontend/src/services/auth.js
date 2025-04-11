import axios from "axios";
import config from "../config"

export default class AuthService {
    async #getResponse(callback) {
        try {
            const response = await callback();
            return {success: true, data: response.data}
        } catch (error) {
            console.error("Invalid request", error.message);
            return {success: false, data: error.response.data}
        }
    }

    async login({email, password}) {
        const data = JSON.stringify({email, password})
        return await this.#getResponse(() =>
            axios.post(`https://${config.HOST}/api/token/set/`, data, {
                headers: {
                    "Content-Type": "application/json"
                },
                withCredentials: true
            })
        )
    }

    async logout() {
        return await this.#getResponse(() =>
            axios.post(`https://${config.HOST}/api/token/delete/`, null, {
                withCredentials: true
            })
        )
    }

    async isAuthenticated() {
        return await this.#getResponse(() =>
            axios.get(`https://${config.HOST}/api/me/`, {
                withCredentials: true
            })
        )
    }
}