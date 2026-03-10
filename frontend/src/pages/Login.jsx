import { useState } from "react";

function Login() {
  const [username, setUsername] = useState("");

  const handleLogin = () => {
    localStorage.setItem("username", username);
    window.location.href = "/chat";
  };

  return (
    <div>
      <h2>Login</h2>

      <input
        placeholder="Enter username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <button onClick={handleLogin}>
        Join Chat
      </button>
    </div>
  );
}

export default Login;