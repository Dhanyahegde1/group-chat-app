import React, { useState, useEffect, useCallback } from "react";
import ChannelList from "../components/ChannelList";
import MessageList from "../components/MessageList";
import MessageInput from "../components/MessageInput";
import DMWindow from "../components/DMWindow";
import axios from "axios";
import "../styles/styles.css";
import NotificationBell from "../components/NotificationBell";

function Chat() {
  const [activeChannel, setActiveChannel] = useState(null);
  const [activeDM,      setActiveDM]      = useState(null); // other user's username
  const [inviteLink,    setInviteLink]     = useState("");
  const [showInvite,    setShowInvite]     = useState(false);
  const [pendingInvite, setPendingInvite]  = useState(null);
  const [activeChannelId, setActiveChannelId] = useState(null);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [offlineUsers, setOfflineUsers] = useState([]);

  const handleUsersUpdate = useCallback((online, offline)  => {
    setOnlineUsers(online);
    setOfflineUsers(offline);
}, []); 

  const handleInvite = async () => {
  try {
    const res = await axios.post("http://127.0.0.1:8000/channels/invite/generate/", {
      channel_id: activeChannelId   // ← use actual channel id
    });
    setInviteLink(res.data.invite_link);
    setShowInvite(true);
  } 
  catch {
    alert("Failed to generate invite link");
  }
};

useEffect(() => {
  const interval = setInterval(async () => {
    if (!activeChannelId) return;
    try {
      const res = await axios.get(`http://127.0.0.1:8000/channels/invite/pending/${activeChannelId}/`);
      if (res.data.code) {
        setPendingInvite(res.data);
      }

    } catch (error) {
      console.error(error);
    }
  }, 3000);
  return () => clearInterval(interval);
}, [activeChannelId]);


  const handleRespond = async (action) => {
    try {
      await axios.post("http://127.0.0.1:8000/channels/invite/respond/", {
        code: pendingInvite.code,
        action
      });
      setPendingInvite(null);
    } catch (err) {
      console.error(err);
    }
  };

  // When user picks a channel, clear DM and vice versa
 const handleChannelSelect = (channelName, channelId) => {
  setActiveChannel(channelName);
  setActiveChannelId(channelId);
  setActiveDM(null);
};

  const handleDMSelect = (otherUsername, otherUserId) => {
  setActiveDM({
    username: otherUsername,
    id: otherUserId
  });

  setActiveChannel(null);
  setActiveChannelId(null);
};

  return (
    <div className="chat-container">

      {/* LEFT SIDEBAR */}
      <div className="sidebar">
        <ChannelList
          activeChannel={activeChannel}
          onChannelSelect={handleChannelSelect}
          onDMSelect={handleDMSelect}
        />
      </div>

      {/* MAIN AREA */}
      <div className="chat-main">

        {/* ── Channel chat ── */}
        {activeChannel && (
          <>

            <div className="chat-header" >
 
  <h2> {activeChannel}</h2>
  <div className="online-bar">
    {onlineUsers.map((u, i) => (
      <span key={i} className="online-user">🟢 {u}</span>
    ))}
    {offlineUsers
      .filter((u) => u !== localStorage.getItem("username"))
      .map((u, i) => (
        <span key={i} className="offline-user">🔴 {u}</span>
      ))
    }
  </div>
   <NotificationBell /> 
  <button className="invite-btn" onClick={handleInvite}>Invite</button>
</div>

            {showInvite && (
              <div className="invite-popup">
                <p>Share this link:</p>
                <input readOnly value={inviteLink} />
                <button onClick={() => { navigator.clipboard.writeText(inviteLink); alert("Copied!"); }}>Copy</button>
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

            
           <MessageList activeChannel={activeChannel} onUsersUpdate={handleUsersUpdate} />
                <MessageInput activeChannel={activeChannel} channelId={activeChannelId} />
             
          </>
        )}

        {/* ── Direct message ── */}
        {activeDM && (
          <>
            <div className="chat-header">
              <h2>💬 {activeDM.username}</h2>
               <NotificationBell />
            </div>
            <DMWindow 
              otherUsername={activeDM.username}
              otherUserId={activeDM.id}/>

          </>
        )}

        {/* ── Nothing selected ── */}
        {!activeChannel && !activeDM && (
          <div style={{ padding: "40px", color: "#888" }}>
            Select a channel or user to start chatting.
             <NotificationBell />
          </div>
        )}

      </div>
    </div>
  );
}

export default Chat;