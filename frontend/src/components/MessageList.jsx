import React, { useState, useEffect } from "react";
import { connectToRoom, disconnectRoom } from "../services/websocket";

function MessageList({ activeChannel }) {

  const currentUser = localStorage.getItem("username");
  const roomName = activeChannel; 

  const [messages, setMessages] = useState([]);
  const [typingUser, setTypingUser] = useState("");
  const [allRead, setAllRead] = useState(false);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [offlineUsers, setOfflineUsers] = useState([]);

  useEffect(() => {
    setMessages([]);      // ← clear old messages
    setOnlineUsers([]);   // ← clear old online users
    setAllRead(false);    // ← reset read status
    disconnectRoom();
    connectToRoom(
      roomName,
      currentUser,  

      // onMessage — new message received
       (data) => {
        setMessages((prev) => [...prev, {
          user: data.username,
          text: data.message,
          timestamp: data.timestamp
        }]);
        
      },

      // onTyping — someone is typing
      (username) => {
        setTypingUser(username);
        setTimeout(() => setTypingUser(""), 2000);
      },

      // onHistory — load old messages on connect
            (history) => {
        setMessages(history.map((m) => ({
          user: m.username,
          text: m.message,
          timestamp: m.timestamp
        })));
      },

       // onRead
      () => { setAllRead(true); },

      // onOnline
      (username) => {
        setOnlineUsers((prev) => [...new Set([...prev, username])]);
      },

      // onOffline
       (username) => {
        setOnlineUsers((prev) => prev.filter((u) => u !== username));
        setOfflineUsers((prev) => [...new Set([...prev, username])]);
    }
    );
    
    
    return () => disconnectRoom();

  }, [activeChannel, currentUser, roomName]);

  const renderMessage = (text) => {
  if (!text) return text;
  const fileLinkRegex = /📎 \[(.+?)\]\((https?:\/\/.+?)\)/;
  const match = text.match(fileLinkRegex);
  if (match) {
    const [, filename, url] = match;
    const isImage = /\.(jpg|jpeg|png|gif)$/i.test(filename);
    if (isImage) {
      return (
        <a href={url} target="_blank" rel="noreferrer">
          <img src={url} alt={filename} style={{ maxWidth: "200px", borderRadius: "8px" }} />
        </a>
      );
    }
    return <a href={url} target="_blank" rel="noreferrer">📎 {filename}</a>;
  }
  return text;
};
  return (
    <div className="message-list">

      {/* Online users and offline users*/}
      <div className="online-bar">
    {onlineUsers.map((u, i) => (
        <span key={i} className="online-user">🟢 {u}</span>
    ))}
    {offlineUsers.map((u, i) => (
        <span key={i} className="offline-user">🔴 {u}</span>
    ))}
</div>

     {/* Messages */}
      {messages.map((msg, i) => (
        <div
          key={i}
          className={msg.user === currentUser ? "message my-message" : "message other-message"}
        >
          <span className="msg-user">{msg.user}</span>
          <p>{renderMessage(msg.text)}</p>
          <div className="msg-meta">
            <span className="msg-time">{msg.timestamp}</span>
            {msg.user === currentUser && (
              <span className="tick">
                {allRead ? "✓✓" : "✓"}
              </span>
            )}
          </div>
        </div>
      ))}

      {typingUser && (
        <div className="typing-indicator">
          {typingUser} is typing...
        </div>
      )}

    </div>
  );
}

export default MessageList;