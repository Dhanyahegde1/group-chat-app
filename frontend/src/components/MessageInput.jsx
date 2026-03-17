import { useState } from "react";
import { sendMessage, sendTyping } from "../services/websocket";
import { uploadFile } from "../services/api";

function MessageInput({ activeChannel, channelId }) {

  const [message, setMessage] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const username = localStorage.getItem("username");

  const handleSend = async () => {
    // Normal text message
    if (message.trim()) {
      sendMessage(message, username);
      setMessage("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSend();
  };

  const handleTyping = (e) => {
    setMessage(e.target.value);
    sendTyping(username);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    // If file exists → upload first
    if (!file)return alert("No file selected.")
    if (!channelId) {
        alert("No channel selected.");
        return;
      }
      console.log("uploading to channel:", channelId);
      const formData = new FormData();
      formData.append("file", file);
      formData.append("username", username);
      formData.append("channel_id", channelId);

      try {
        setLoading(true);
        const res = await uploadFile(formData);
        const fileUrl = `http://127.0.0.1:8000/media/uploads${res.data.filename}`;
        const fileMsg = `📎 [${res.data.filename}](${fileUrl})`;
        // Send file message to websocket
        sendMessage(fileMsg, username);
        setFile(null);
        document.getElementById("channelFileInput").value = "";
        } 
      catch (err) {
        const msg = err.response?.data?.error || "Upload failed.";
        alert(msg);
      } 
      finally {
        setLoading(false);
      }
    }
  return (

    <div className="message-input">
      <input
        type="text"
        placeholder="Type your message..."
        value={message}
        onChange={handleTyping}
        onKeyDown={handleKeyDown}
      />

      <input
        type="file"
        id="channelFileInput"
        style={{ display: "none" }}
        accept=".pdf,.doc,.docx,.jpg,.jpeg,.csv,.xls,.xlsx"
        onChange={handleFileChange}
      />

      <button onClick={() => document.getElementById("channelFileInput").click()}>
       Upload
      </button>

      {file && (
        <span style={{ fontSize: "12px", color: "#aaa", marginLeft: "5px" }}>
          {file.name}
          <button onClick={handleFileUpload} disabled={loading}>
            {loading ? "Sending..." : "Send"}
          </button>
        </span>
      )}

      <button onClick={handleSend} disabled={loading}>Send</button>
    </div>
  );
}

export default MessageInput;