import React, { useState, useEffect } from "react";
import { connectToRoom, disconnectRoom } from "../services/websocket";

function MessageList({ activeChannel, onUsersUpdate }) {

  const currentUser = localStorage.getItem("username");
  const roomName = activeChannel; 

  const [messages, setMessages] = useState([]);
  const [typingUser, setTypingUser] = useState("");
  const [allRead, setAllRead] = useState(false);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [offlineUsers, setOfflineUsers] = useState([]);

// eslint-disable-next-line
  useEffect(() => {
    setMessages([]);      // ← clear old messages
    setOnlineUsers([]);   // ← clear old online users
    setOfflineUsers([]);
    setAllRead(false);    // ← reset read status
    disconnectRoom();

  connectToRoom(
    roomName,
    currentUser,

  // onMessage
  (data) => {
    setMessages((prev) => [...prev, {
      user: data.username,
      text: data.message,
      timestamp: data.timestamp
    }]);
  },

  // onTyping
  (username) => {
    setTypingUser(username);
    setTimeout(() => setTypingUser(""), 2000);
  },

  // onHistory
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
    setOfflineUsers((prev) => {
      const newOffline = prev.filter((u) => u !== username);
      setOnlineUsers((prevOnline) => {
        const newOnline = [...new Set([...prevOnline, username])];
        onUsersUpdate(newOnline, newOffline);  // ← add this
        return newOnline;
      });
      return newOffline;
    });
  },

// onOffline
(username) => {
    setOnlineUsers((prev) => {
      const newOnline = prev.filter((u) => u !== username);
      setOfflineUsers((prevOffline) => {
        const newOffline = [...new Set([...prevOffline, username])];
        onUsersUpdate(newOnline, newOffline);  // ← add this
        return newOffline;
      });
      return newOnline;
    });
  }
);
    
return () => disconnectRoom();
}, [activeChannel, currentUser, roomName, onUsersUpdate ]);

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

     {/* Messages */}
      {messages.map((msg, i) => (
        <div
          key={i}
          className={msg.user === currentUser ? "message my-message" : "message other-message"}
        >
          <span className="msg-user">{msg.user}</span>
         <p>{msg.text && renderMessage(msg.text)}</p>
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