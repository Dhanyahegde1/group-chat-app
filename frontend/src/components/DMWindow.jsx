import React, { useState, useEffect, useRef } from "react";
import { connectToDM, sendDMMessage, sendDMTyping, disconnectDM } from "../services/websocket";
import axios from "axios";

function DMWindow({ otherUsername, otherUserId }){
  const [messages,   setMessages]   = useState([]);
  const [input,      setInput]      = useState("");
  const [typingUser, setTypingUser] = useState("");
  const [file,       setFile]       = useState(null);
  const [loading,    setLoading]    = useState(false);
  const typingTimer = useRef(null);
  const bottomRef   = useRef(null);

  const myUsername = localStorage.getItem("username");

  useEffect(() => {
    setMessages([]);
    connectToDM(
      myUsername,
      otherUsername,
      (msg)     => setMessages(prev => [...prev, msg]),
      (sender)  => { setTypingUser(sender); setTimeout(() => setTypingUser(""), 2000); },
      (history) => setMessages(history),
    );
    return () => disconnectDM();
  }, [otherUsername, myUsername]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    sendDMMessage(input.trim());
    setInput("");
  };

  const handleTyping = (e) => {
    setInput(e.target.value);
    sendDMTyping();
    clearTimeout(typingTimer.current);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSend();
  };

  const handleFileChange = async (e) => {

  const selected = e.target.files[0];
  if (!selected) return;

  const formData = new FormData();
  formData.append("file", selected);
  formData.append("username", myUsername);
  formData.append("receiver_id", otherUserId);

  try {

    const res = await axios.post(
      "http://127.0.0.1:8000/files/upload/",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );

    const fileUrl = `http://127.0.0.1:8000/media/${res.data.filename}`;
    const fileMsg = `📎 [${res.data.filename}](${fileUrl})`;

    sendDMMessage(fileMsg);

  } catch (err) {

    const msg = err.response?.data?.error || "Upload failed.";
    alert(msg);

  }

};
 console.log("Receiver ID:", otherUserId);
 const handleFileUpload = async () => {
  if (!file) return alert("No file selected.");

  const formData = new FormData();
  formData.append("file", file);
  formData.append("username", myUsername);
  formData.append("receiver_id", otherUserId);

  try {
    setLoading(true);

    const res = await axios.post(
      "http://127.0.0.1:8000/files/upload/",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );

    const fileUrl = `http://127.0.0.1:8000/media/${res.data.filename}`;
    const fileMsg = `📎 [${res.data.filename}](${fileUrl})`;

    sendDMMessage(fileMsg);

    setFile(null);
    document.getElementById("dmFileInput").value = "";

  } catch (err) {
    const msg = err.response?.data?.error || "Upload failed.";
    alert(msg);
  } finally {
    setLoading(false);
  }
};

  // Render message — if it's a file link, show as clickable
  const renderMessage = (text) => {
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
    <div className="message-area" style={{ display: "flex", flexDirection: "column", height: "100%" }}>

      <div className="message-list">
        {messages.map((m, i) => (
          <div
            key={i}
            className={m.sender === myUsername ? "message my-message" : "message other-message"}
          >
            <span className="msg-user">{m.sender}</span>
            <p>{renderMessage(m.message)}</p>
            <div className="msg-meta">
              <span className="msg-time">{m.timestamp}</span>
              {m.sender === myUsername && <span className="tick">✓</span>}
            </div>
          </div>
        ))}

        {typingUser && <div className="typing-indicator">{typingUser} is typing…</div>}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="message-input" style={{ display: "flex", padding: "10px" }}>
        <input
          value={input}
          onChange={handleTyping}
          onKeyDown={handleKeyDown}
          placeholder={`Message ${otherUsername}…`}
          style={{ flex: 1 }}
        />

        <input
          type="file"
          id="dmFileInput"
          style={{ display: "none" }}
          accept=".pdf,.doc,.docx,.jpg,.jpeg,.csv,.xls,.xlsx"
          onChange={handleFileChange}
        />

        <button onClick={() => document.getElementById("dmFileInput").click()}>📎</button>

        {file && (
          <span style={{ fontSize: "12px", color: "#aaa" }}>
            {file.name}
            <button onClick={handleFileUpload} disabled={loading}>
              {loading ? "Uploading…" : "Upload"}
            </button>
          </span>
        )}

        <button onClick={handleSend}>Send</button>
      </div>

    </div>
  );
}

export default DMWindow;