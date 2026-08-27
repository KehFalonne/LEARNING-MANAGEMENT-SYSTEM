import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
});

// Automatically attach the JWT access token
// to every authenticated API request.
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Base URL for uploaded media/files
export const MEDIA_URL = "http://127.0.0.1:8000";

export default api;