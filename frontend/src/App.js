import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
// import axios from "axios";
import JoinPage from "./pages/JoinPage";


function App() {
  return (
    
    <Router>
      <div className="particles">
  {Array.from({length:25}).map((_,i)=>(
    <span key={i}
      style={{
        left:Math.random()*100+"%",
        animationDuration:(5+Math.random()*10)+"s",
        animationDelay:(Math.random()*5)+"s"
      }}
    ></span>
  ))}
</div>
      <Routes>
        
        <Route path="/" element={<Login />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/join/:code" element={<JoinPage />} />

      </Routes>
    </Router>
  );
}


export default App;
