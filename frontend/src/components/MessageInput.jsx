import React, { useState } from "react";

function MessageInput() {

  const [message, setMessage] = useState("");

  const sendMessage = () => {
    console.log("Message:", message);
    setMessage("");
  };

  return (
    <div className="message-input">

      <input
        type="text"
        placeholder="Type your message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <button onClick={sendMessage}>
        Send
      </button>

    </div>
  );
}

export default MessageInput;