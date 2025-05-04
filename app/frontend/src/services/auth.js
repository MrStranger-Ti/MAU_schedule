import axios from "axios";
import {config} from "../config"
import BaseService from "./base";
import {pagesPaths} from "../config";

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

    async register({full_name, password, email, course, institute, group}) {
        const registerResponse = await this.getResponse(() =>
            axios.post(`https://${config.API_HOST}/api/register/`, {
                user: {
                    full_name,
                    password,
                    email,
                    course,
                    institute,
                    group
                },
                options: {
                    url: `https://${window.location.host}${pagesPaths.accounts.baseRegisterConfirm}`
                }
            })
        )
        return {
            success: registerResponse.success,
            data: registerResponse.data.user
        }
    }

    async registerConfirm({uidb64, token}) {
        return await this.getResponse(() =>
            axios.get(`https://${config.API_HOST}/api/register/confirm/${uidb64}/${token}/`)
        )
    }

    async passwordReset({email}) {
        return await this.getResponse(() =>
            axios.post(`https://${config.API_HOST}/api/password/reset/`, {
                email,
                options: {
                    url: `https://${window.location.host}${pagesPaths.accounts.basePasswordResetConfirm}`
                }
            })
        )
    }

    async passwordResetConfirm({uidb64, token}, {password1, password2}) {
        return await this.getResponse(() =>
            axios.post(`https://${config.API_HOST}/api/password/reset/confirm/${uidb64}/${token}/`, {
                password1,
                password2
            })
        )
    }
}