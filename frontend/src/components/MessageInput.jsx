import React, { useState } from "react";
import { uploadFile } from "../services/api";

function MessageInput() {

  const [message, setMessage] = useState("");
   const [file, setFile] = useState(null);

  const username = localStorage.getItem("username");
  const channel_id = 1; // replace with real channel later

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("username", username);
    formData.append("channel_id", channel_id);

    try {
      await uploadFile(formData);
      alert("File uploaded successfully!");
      setFile(null);
    } catch (error) {
      alert("Upload failed. Check file type and size.");
    }
  };


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
      {/* Hidden file input */}
      <input
        type="file"
        id="fileInput"
        style={{ display: "none" }}
        accept=".pdf,.doc,.docx,.jpg,.jpeg,.csv,.xls,.xlsx"
        onChange={handleFileChange}
      />

      {/* Paperclip button */}
      <button onClick={() => document.getElementById("fileInput").click()}>
        📎
      </button>

      {/* Show selected filename */}
      {file && (
        <span>{file.name}
          <button onClick={handleFileUpload}>Upload</button>
        </span>
      )}

      <button onClick={sendMessage}>
        Send
      </button>

    </div>
  );
}

export default MessageInput;