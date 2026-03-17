let socket = null;

export const connectToRoom = (roomName, username, onMessage, onTyping, onHistory, onRead, onOnline, onOffline) => {
  socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${roomName}/${username}/`);
  
  socket.onopen = () => console.log("Connected to room:", roomName);

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if      (data.type === "chat_history")  onHistory(data.messages);
    else if (data.type === "chat_message")  onMessage(data);
    else if (data.type === "typing")        onTyping(data.username);
    else if (data.type === "messages_read") onRead();
    else if (data.type === "user_online")   onOnline(data.username);
    else if (data.type === "user_offline")  onOffline(data.username);
  };

  socket.onclose = (e) => {
    if (e.code === 4003) console.warn("Access denied: not a member.");
    else console.log("Disconnected from room:", roomName);
  };

  socket.onerror = (error) => console.error("WebSocket error:", error);
};

export const sendMessage = (message, username) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: "chat_message", message, username }));
  }
};

export const sendTyping = (username) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: "typing", username }));
  }
};

export const disconnectRoom = () => {
  if (socket) socket.close();
};


let dmSocket = null;

export const connectToDM = (myUsername, otherUsername, onMessage, onTyping, onHistory) => {
  dmSocket = new WebSocket(`ws://127.0.0.1:8000/ws/dm/${myUsername}/${otherUsername}/`);

  dmSocket.onopen = () => console.log(`DM connected: ${myUsername} ↔ ${otherUsername}`);

  dmSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if      (data.type === "dm_history") onHistory(data.messages);
    else if (data.type === "dm_message") onMessage(data);
    else if (data.type === "typing")     onTyping(data.sender);
  };

  dmSocket.onclose = () => console.log("DM disconnected");
  dmSocket.onerror = (e) => console.error("DM WebSocket error:", e);
};

export const sendDMMessage = (message) => {
  if (dmSocket && dmSocket.readyState === WebSocket.OPEN) {
    dmSocket.send(JSON.stringify({ type: "dm_message", message }));
  }
};

export const sendDMTyping = () => {
  if (dmSocket && dmSocket.readyState === WebSocket.OPEN) {
    dmSocket.send(JSON.stringify({ type: "typing" }));
  }
};
export const disconnectDM = () => {
  if (dmSocket) dmSocket.close();
};