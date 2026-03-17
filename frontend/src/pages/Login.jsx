import { useState } from "react";
import { loginUser } from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/styles.css";

function Login() {

   const navigate = useNavigate(); 
  const [form, setForm] = useState({
    username: "",
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
    const res = await loginUser(form);
    localStorage.setItem("username", res.data.username);
    localStorage.setItem("userId", res.data.id);  
    alert("Login successful! Welcome " + res.data.username);
    navigate("/chat");
  } catch (error) {
    alert("Invalid username or password");
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

      <h2>Login</h2>

      <form onSubmit={handleSubmit}>

        <input
          name="username"
          placeholder="Username"
          onChange={handleChange}
        />

        <input
          name="password"
          type="password"
          placeholder="Password"
          onChange={handleChange}
        />

        <button type="submit">
          Login
        </button>

      </form>
       <br />

      <button onClick={() => navigate("/register")}>

        Create Account

      </button>

    </div>
  );
}

export default Login;