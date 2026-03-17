import axios from "axios";

const API = axios.create({
  baseURL: "http://192.168.31.133:8000",
});

export const registerUser  = (data) => API.post("/users/register/", data);
export const loginUser     = (data) => API.post("/users/login/", data);
export const getChannels      = () => API.get("/channels/");
export const getMyChannels = (userId) => API.get(`/channels/my/?user=${userId}`);
export const discoverChannels = (userId) => API.get(`/channels/discover/?user=${userId}`);
export const createChannel    = (data) => API.post("/channels/create/", data);
export const joinChannel      = (data) => API.post("/channels/join/", data);
export const leaveChannel     = (data) => API.delete("/channels/leave/", { data });
export const uploadFile = (formData) => API.post("/files/upload/", formData);
export const getDMHistory = (myUsername, otherUsername) =>
  API.get(`/messages/dm/${myUsername}/${otherUsername}/`);