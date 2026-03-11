import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const registerUser = (data) => API.post("/users/register/", data);
export const loginUser = (data) => API.post("/users/login/", data);
export const getChannels = () => API.get("/channels");
export const createChannel = (data) => API.post("/channels/create", data);