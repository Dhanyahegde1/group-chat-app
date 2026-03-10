let socket;

export const connectSocket = (room) => {
  socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${room}/`);

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Message:", data);
  };
};

export const sendMessage = (message) => {
  socket.send(JSON.stringify({ message }));
};