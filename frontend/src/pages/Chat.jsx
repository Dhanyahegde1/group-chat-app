import ChannelList from "../components/ChannelList";
import MessageList from "../components/MessageList";
import MessageInput from "../components/MessageInput";

function Chat() {
  return (
    <div>

      <h2>Group Chat</h2>

      <ChannelList />

      <MessageList />

      <MessageInput />

    </div>
  );
}

export default Chat;