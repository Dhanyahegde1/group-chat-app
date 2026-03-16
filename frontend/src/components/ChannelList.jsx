import React, { useState, useEffect } from "react";
import axios from "axios";

function ChannelList({ activeChannel, onChannelSelect }) {

  const [channels, setChannels] = useState([]);
  const [showCreate, setShowCreate] = useState(false);
  const [newChannelName, setNewChannelName] = useState("");
  const username = localStorage.getItem("username");
  const userId = localStorage.getItem("userId");

  // Load channels from backend
  useEffect(() => {
    const fetchChannels = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/channels/");
        console.log("Channels fetched:", res.data);
        setChannels(res.data);
      } catch (error) {
        console.error("Failed to fetch channels", error);
      }
    };
    fetchChannels();
  }, []);

  // Create new channel
  const handleCreate = async () => {
    if (!newChannelName.trim()) return;
    try {
      const res = await axios.post("http://127.0.0.1:8000/channels/create/", {
        name: newChannelName,
        created_by: userId  
      });
      setChannels([...channels, { id: res.data.id, name: newChannelName }]);
      setNewChannelName("");
      setShowCreate(false);
    } catch (error) {
      alert("Failed to create channel");
    }
  };

  return (
    <div className="channel-list">

      <h3>Channels</h3>

      <ul>
        {channels.map((c) => (
          <li
            key={c.id}
            onClick={() => onChannelSelect(c.name)}
            className={c.name === activeChannel ? "active-channel" : ""}
            style={{ cursor: "pointer" }}
          >
            # {c.name}
          </li>
        ))}
      </ul>

      <button onClick={() => setShowCreate(!showCreate)}>
        + Create Room
      </button>

      {showCreate && (
        <div>
          <input
            placeholder="Channel name"
            value={newChannelName}
            onChange={(e) => setNewChannelName(e.target.value)}
          />
          <button onClick={handleCreate}>Create</button>
          <button onClick={() => setShowCreate(false)}>Cancel</button>
        </div>
      )}

    </div>
  );
}

export default ChannelList;