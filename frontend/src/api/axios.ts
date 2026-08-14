import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Create an interceptor to add the token to every request
API.interceptors.request.use(
  (config) => {
    // 1. Get the token from localStorage (or context)
    const token = localStorage.getItem("token"); 

    // 2. If the token exists, add it to the Authorization header
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }

    // 3. Return the modified config
    return config;
  },
  (error) => {
    // Handle request errors
    return Promise.reject(error);
  }
);

export default API;