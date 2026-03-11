import React from "react";

function ChannelList() {

  const channels = [
    "General",
    "Project",
    "Random"
  ];

  return (
    <div className="channel-list">

      <h3>Channels</h3>

      <button className="create-channel">
        + Create Room
      </button>

      <ul>
        {channels.map((c, index) => (
          <li key={index}>{c}</li>
        ))}
      </ul>

    </div>
  );
}

export default ChannelList;