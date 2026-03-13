import { useState } from "react";
import { sendMessage, sendTyping } from "../services/websocket";
import { uploadFile } from "../services/api";

function MessageInput() {

  const [message, setMessage] = useState("");
  const [file, setFile] = useState(null);
  const username = localStorage.getItem("username");

  const handleSend = () => {
    if (message.trim()) {
      sendMessage(message, username);
      setMessage("");
    }
  };

  const handleTyping = (e) => {
    setMessage(e.target.value);
    sendTyping(username);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    formData.append("username", username);
    formData.append("channel_id", 1);
    try {
      await uploadFile(formData);
      alert("File uploaded successfully!");
      setFile(null);
    } catch (error) {
      alert("Upload failed.");
    }
  };

  return (
    <div className="message-input">

      <input
        type="text"
        placeholder="Type your message..."
        value={message}
        onChange={handleTyping}
      />

      <input
        type="file"
        id="fileInput"
        style={{ display: "none" }}
        accept=".pdf,.doc,.docx,.jpg,.jpeg,.csv,.xls,.xlsx"
        onChange={handleFileChange}
      />

      <button onClick={() => document.getElementById("fileInput").click()}>
        📎
      </button>

      {file && (
        <span>{file.name}
          <button onClick={handleFileUpload}>Upload</button>
        </span>
      )}

      <button onClick={handleSend}>Send</button>

    </div>
  );
}

export default MessageInput;