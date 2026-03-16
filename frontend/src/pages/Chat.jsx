import ChannelList from "../components/ChannelList";
import MessageList from "../components/MessageList";
import MessageInput from "../components/MessageInput";
import "../styles/styles.css";
import axios from "axios";
import React, { useState, useEffect } from "react";

function Chat() {
  const [inviteLink, setInviteLink] = useState("");
  const [showInvite, setShowInvite] = useState(false);
  const [activeChannel, setActiveChannel] = useState("General");
  const [pendingInvite, setPendingInvite] = useState(null);

  const handleInvite = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/channels/invite/generate/", {
        channel_id: 1
      });
      setInviteLink(res.data.invite_link);
      setShowInvite(true);
    } catch (error) {
      alert("Failed to generate invite link");
    }
  };

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/channels/invite/pending/1/");
        if (res.data.code) {
          setPendingInvite(res.data);
        }
      } catch (error) {
        console.error(error);
      }
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleRespond = async (action) => {
    try {
      await axios.post("http://127.0.0.1:8000/channels/invite/respond/", {
        code: pendingInvite.code,
        action: action
      });
      setPendingInvite(null);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(inviteLink);
    alert("Invite link copied!");
  };

  return (
    <div className="chat-container">

      {/* LEFT PANEL */}
      <div className="sidebar">
        <ChannelList
          activeChannel={activeChannel}
          onChannelSelect={setActiveChannel}
        />
      </div>

      {/* RIGHT PANEL */}
      <div className="chat-main">

        <div className="chat-header">
          <h2>Chatroom  {activeChannel}</h2>
          <button className="invite-btn" onClick={handleInvite}>
            Invite
          </button>
        </div>

        {showInvite && (
          <div className="invite-popup">
            <p>Share this link:</p>
            <input readOnly value={inviteLink} />
            <button onClick={handleCopy}>Copy</button>
            <button onClick={() => setShowInvite(false)}>Close</button>
          </div>
        )}

        {pendingInvite && (
          <div className="invite-popup">
            <p>{pendingInvite.username} wants to join!</p>
            <button onClick={() => handleRespond("accept")}>✅ Allow</button>
            <button onClick={() => handleRespond("decline")}>❌ Decline</button>
          </div>
        )}

        <MessageList activeChannel={activeChannel} />
        <MessageInput activeChannel={activeChannel} />

      </div>

    </div>
  );
}

export default Chat;