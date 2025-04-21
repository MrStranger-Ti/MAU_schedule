export default class BaseService {
    async getResponse(callback) {
        try {
            const response = await callback();
            return {success: true, data: response.data}
        } catch (error) {
            console.error("Invalid request", error.message);
            // console.log(error.response.data)
            return {success: false, data: error.response.data}
        }
    }
}