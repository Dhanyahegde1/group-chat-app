import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api"
});

export const registerUser = (data) => API.post("/register", data);

export const loginUser = (data) => API.post("/login", data);

export const getChannels = () => API.get("/channels");

export const createChannel = (data) => API.post("/channels", data);

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />

      </Routes>
    </Router>
  );
}


export default App;
