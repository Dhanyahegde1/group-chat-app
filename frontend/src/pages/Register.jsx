import { useState } from "react";
import { registerUser } from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/styles.css";

function Register() {

  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: ""
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    await registerUser(form);
    alert("Registered successfully! Please log in.");
    navigate("/");
  } catch (error) {
    alert("Registration failed. Username may be taken or password too weak.");
    console.error(error);
  }
};

  return (
    <div className="auth-card">
      <div className="app-title">
    ChatRoom
  </div>

  <div className="app-subtitle">
    Group Chat Application
  </div>

      <h2>Register</h2>

      <form onSubmit={handleSubmit}>

        <input
          name="username"
          placeholder="Username"
          onChange={handleChange}
        />

        <input
          name="email"
          placeholder="Email"
          onChange={handleChange}
        />

        <input
          name="password"
          type="password"
          placeholder="Password"
          onChange={handleChange}
        />

        <button type="submit">
          Register
        </button>

      </form>

      <br/>

      <button onClick={() => navigate("/")}>
        Back to Login
      </button>
    </div>
  );
}

export default Register;