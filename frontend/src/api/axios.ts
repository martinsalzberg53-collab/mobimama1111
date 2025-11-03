import axios from "axios";



const API = axios.create({
  baseURL: "http://localhost:8000/api",  // django backend URL . Replace later with env variable when deploying
  headers: {
    "Content-Type": "application/json",
  },
});

export default API;