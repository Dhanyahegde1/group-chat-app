import React from "react";

function MessageList() {

 const currentUser = localStorage.getItem("username");

  const messages = [
    { user: "tom", text: "Hello everyone" },
    { user: "Rahul", text: "Hi!" },
    { user: "tom", text: "How are you?" }
  ];

  return (
    <div className="message-list">

      {messages.map((msg, i) => (

        <div
          key={i}
          className={
            msg.user === currentUser
            ? "message my-message"
            : "message other-message"
          }
        >
          <span className="msg-user">{msg.user}</span>
          <p>{msg.text}</p>
        </div>

      ))}

    </div>
  );
}

export default MessageList;