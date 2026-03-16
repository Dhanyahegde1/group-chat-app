import React from "react";
import axios from "axios";
import { sendMessage } from "../services/websocket";

function FileUpload({ channelId }) {

  const username = localStorage.getItem("username");

  const handleFileChange = async (e) => {

    const selected = e.target.files[0];
    if (!selected) return;

    const formData = new FormData();
    formData.append("file", selected);
    formData.append("username", username);
    formData.append("channel_id", channelId);

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/files/upload/",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      const fileUrl = `http://127.0.0.1:8000/media/${res.data.filename}`;
      const fileMsg = `📎 [${res.data.filename}](${fileUrl})`;

      sendMessage(fileMsg, username);

    } catch (err) {

      const msg = err.response?.data?.error || "Upload failed.";
      alert(msg);

    }

  };

  return (
    <div style={{ padding: "6px", borderTop: "1px solid #333" }}>

      <input
        id="channelFileInput"
        type="file"
        style={{ display: "none" }}
        accept=".pdf,.doc,.docx,.jpg,.jpeg,.csv,.xls,.xlsx"
        onChange={handleFileChange}
      />

      <button
        onClick={() => document.getElementById("channelFileInput").click()}
      >
        📎
      </button>

    </div>
  );
}

export default FileUpload;
