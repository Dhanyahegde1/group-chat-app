import { useEffect, useState } from "react";
import { getChannels } from "../services/api";
import "../styles/dashboard.css";

function Dashboard() {

  const [channels, setChannels] = useState([]);
  const userId = localStorage.getItem("userId");

  useEffect(() => {

    const fetchChannels = async () => {

      const res = await getMyChannels(userId);

      setChannels(res.data);

    };

    fetchChannels();

  }, []);

  return (

    <div>

      <h2>Chat Rooms</h2>

      <ul>

        {channels.map((c) => (

          <li key={c.id}>
            {c.name}
          </li>

        ))}

      </ul>

    </div>

  );

}

export default Dashboard;