import { useState } from "react";

function MessageInput() {

  const [message, setMessage] = useState("");

  const sendMessage = () => {
    console.log(message);
    setMessage("");
  };

  return (
    <div>

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type message"
      />

      <button onClick={sendMessage}>
        Send
      </button>

    </div>
  );
}

export default MessageInput;