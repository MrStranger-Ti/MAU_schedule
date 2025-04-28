export default class BaseService {
    async getResponse(callback) {
        try {
            const response = await callback();
            return {success: true, data: response.data}
        } catch (error) {
            return {success: false, data: error.response.data}
        }
    }
}