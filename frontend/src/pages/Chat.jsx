import React from "react";
import ChannelList from "../components/ChannelList";
import MessageList from "../components/MessageList";
import MessageInput from "../components/MessageInput";
import "../styles/styles.css";

function Chat() {
  return (
    <div className="chat-container">

      <div className="sidebar">
        <ChannelList />
      </div>

      <div className="chat-main">

        <div className="chat-header">
          <h2>ChatRoom Dashboard</h2>
           <button className="invite-btn">
    Invite
  </button>
        </div>

        <MessageList />
        <div className="typing-indicator">
  Rahul is typing...
</div>
        <MessageInput />

      </div>

    </div>
  );
}

export default Chat;