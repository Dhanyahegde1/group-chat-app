import React, { useState, useEffect } from "react";
import { getMyChannels, discoverChannels, createChannel, joinChannel, leaveChannel } from "../services/api";
import axios from "axios";

function ChannelList({ activeChannel, onChannelSelect, onDMSelect }) {
  const [myChannels,   setMyChannels]   = useState([]);
  const [discover,     setDiscover]     = useState([]);
  const [showDiscover, setShowDiscover] = useState(false);
  const [showCreate,   setShowCreate]   = useState(false);
  const [newName,      setNewName]      = useState("");
  const [isPrivate,    setIsPrivate]    = useState(false);

  const username = localStorage.getItem("username");
  const userId   = localStorage.getItem("userId");

  // Load only the user's joined channels
  useEffect(() => {
    fetchMyChannels();
  }, []);

  const fetchMyChannels = async () => {
    try {
      const res = await getMyChannels(userId);
      setMyChannels(res.data);
    } catch (err) {
      console.error("Failed to fetch my channels", err);
    }
  };

  const fetchDiscover = async () => {
    try {
      const res = await discoverChannels(userId);
      setDiscover(res.data);
    } catch (err) {
      console.error("Failed to fetch discover", err);
    }
  };

  const handleCreate = async () => {
    if (!newName.trim()) return;
    try {
      await createChannel({ name: newName, created_by: userId, is_private: isPrivate });
      setNewName("");
      setShowCreate(false);
      fetchMyChannels(); // refresh list — creator is auto-added as member
    } catch {
      alert("Failed to create channel");
    }
  };

  const handleJoin = async (channelId) => {
    try {
      await joinChannel({ user: userId, channel: channelId });
      fetchMyChannels();
      fetchDiscover();
    } catch {
      alert("Failed to join channel");
    }
  };

  const handleLeave = async (e, channelId) => {
    e.stopPropagation(); // don't also select the channel
    try {
      await leaveChannel({ user: userId, channel: channelId });
      fetchMyChannels();
    } catch {
      alert("Failed to leave channel");
    }
  };

  return (
    <div className="channel-list">
      <h3>My Channels</h3>

      <ul>
        {myChannels.map((c) => (
          <li
            key={c.id}
            onClick={() => onChannelSelect(c.name, c.id)}
            className={c.name === activeChannel ? "active-channel" : ""}
            style={{ cursor: "pointer", display: "flex", justifyContent: "space-between" }}
          >
            <span># {c.name}</span>
            <button
              onClick={(e) => handleLeave(e, c.id)}
              style={{ fontSize: "10px", marginLeft: "6px" }}
              title="Leave channel"
            >✕</button>
          </li>
        ))}
      </ul>

      {/* Create channel */}
      <button onClick={() => setShowCreate(!showCreate)}>+ Create Room</button>
      {showCreate && (
        <div>
          <input
            placeholder="Channel name"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
          />
          <label style={{ fontSize: "12px" }}>
            <input
              type="checkbox"
              checked={isPrivate}
              onChange={(e) => setIsPrivate(e.target.checked)}
            /> Private
          </label>
          <button onClick={handleCreate}>Create</button>
          <button onClick={() => setShowCreate(false)}>Cancel</button>
        </div>
      )}

      {/* Discover public channels */}
      <button
        onClick={() => { setShowDiscover(!showDiscover); 
          if (!showDiscover) fetchDiscover(); }}
        style={{ marginTop: "10px" }}
      >
        🔍 Discover
      </button>
      {showDiscover && (
        <ul>
          {discover.length === 0 && <li style={{ fontSize: "12px" }}>No new channels</li>}
          {discover.map((c) => (
            <li key={c.id} style={{ display: "flex", justifyContent: "space-between" }}>
              <span># {c.name}</span>
              <button onClick={() => handleJoin(c.id)} style={{ fontSize: "10px" }}>Join</button>
            </li>
          ))}
        </ul>
      )}

      {/* Direct Messages */}
      {onDMSelect && (
        <div style={{ marginTop: "16px" }}>
          <h3>Direct Messages</h3>
          <DMList onDMSelect={onDMSelect} userId={userId} />
        </div>
      )}
    </div>
  );
}

// ── DM user list (all users except self) ──────────────────────────────────


function DMList({ onDMSelect, userId }) {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/users/list/")
      .then(res => setUsers(res.data.filter(u => String(u.id) !== String(userId))))
      .catch(err => console.error("Failed to load users", err));
  }, []);

  return (
    <ul>
      {users.map(u => (
        <li
          key={u.id}
          onClick={() => onDMSelect(u.username)}
          style={{ cursor: "pointer" }}
        >
          💬 {u.username}
        </li>
      ))}
    </ul>
  );
}

export default ChannelList;