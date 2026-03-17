import React, { useState, useEffect } from "react";
import axios from "axios";

function NotificationBell() {
  const [notifications, setNotifications] = useState([]);
  const [showList, setShowList] = useState(false);
  const userId = localStorage.getItem("userId");

  // Poll for new notifications every 5 seconds
  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await axios.get(`http://192.168.31.133:8000/notifications/${userId}/`);
        setNotifications(res.data);
      } catch (err) {
        console.error("Failed to fetch notifications", err);
      }
    };

    fetchNotifications();
    const interval = setInterval(fetchNotifications, 5000);
    return () => clearInterval(interval);
  }, [userId]);

  const handleMarkAllRead = async () => {
    try {
      await axios.post(`http://192.168.31.133:8000/notifications/${userId}/read-all/`);
      setNotifications([]);
      setShowList(false);
    } catch (err) {
      console.error(err);
    }
  };

  const handleMarkRead = async (id) => {
    try {
      await axios.post(`http://192.168.31.133:8000/notifications/read/${id}/`);
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ position: "relative", display: "inline-block" }}>

      {/* Bell button */}
      <button
        onClick={() => setShowList(!showList)}
        style={{ fontSize: "20px", background: "none", border: "none", cursor: "pointer" }}
      >
        🔔
        {notifications.length > 0 && (
          <span style={{
            background: "red",
            color: "white",
            borderRadius: "50%",
            padding: "2px 6px",
            fontSize: "11px",
            marginLeft: "2px"
          }}>
            {notifications.length}
          </span>
        )}
      </button>

      {/* Notification list */}
      {showList && (
        <div style={{
          position: "absolute",
          right: 0,
          top: "40px",
          width: "280px",
          background: "#1a1a2e",
          border: "1px solid #333",
          borderRadius: "8px",
          zIndex: 999,
          padding: "10px"
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
            <strong>Notifications</strong>
            {notifications.length > 0 && (
              <button onClick={handleMarkAllRead} style={{ fontSize: "11px" }}>
                Mark all read
              </button>
            )}
          </div>

          {notifications.length === 0 && (
            <p style={{ fontSize: "12px", color: "#888" }}>No new notifications</p>
          )}

          {notifications.map((n) => (
            <div
              key={n.id}
              onClick={() => handleMarkRead(n.id)}
              style={{
                padding: "8px",
                borderBottom: "1px solid #333",
                cursor: "pointer",
                fontSize: "13px"
              }}
            >
              <strong>{n.sender}</strong>
              {n.type === "channel" ? ` in #${n.target}` : ` (DM)`}
              <p style={{ margin: "2px 0", color: "#aaa" }}>{n.preview}</p>
              <span style={{ fontSize: "11px", color: "#666" }}>{n.created_at}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default NotificationBell;