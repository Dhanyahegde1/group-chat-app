import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

function JoinPage() {

  const { code } = useParams();
  const navigate = useNavigate();
  const username = localStorage.getItem("username");
  const [status, setStatus] = useState(""); // pending, waiting, accepted, declined

  const handleRequestJoin = async () => {
    try {
      await axios.post(`http://192.168.31.133:8000/channels/invite/join/${code}/`, {  // ← add comma and {
        username: username
      });
      setStatus("waiting");
    } catch (error) {
      setStatus("invalid");
    }
  };
  useEffect(() => {
    let interval;
    if (status === "waiting") {
      // Poll every 3 seconds to check if host accepted
      interval = setInterval(async () => {
        try {
         const res = await axios.get(`http://192.168.31.133:8000/channels/invite/status/${code}/`);
          if (res.data.status === "accepted") {
            setStatus("accepted");
            clearInterval(interval);
            setTimeout(() => navigate("/chat"), 2000);
          } else if (res.data.status === "declined") {
            setStatus("declined");
            clearInterval(interval);
          }
        } catch (error) {
          console.error(error);
        }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [status]);

  return (
    <div className="auth-card">
      <div className="app-title">ChatRoom</div>
      <div className="app-subtitle">Group Chat Application</div>

      <h2>You've Been Invited!</h2>

      {!status && (
        <button onClick={handleRequestJoin}>
          Request to Join
        </button>
      )}

      {status === "waiting" && (
        <p>⏳ Waiting for host to accept...</p>
      )}

      {status === "accepted" && (
        <p>✅ Accepted! Redirecting to chat...</p>
      )}

      {status === "declined" && (
        <p>❌ Your request was declined.</p>
      )}

      {status === "invalid" && (
        <p>❌ Invalid or expired invite link.</p>
      )}
    </div>
  );
}

export default JoinPage;