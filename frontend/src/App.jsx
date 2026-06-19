import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");

  const getMessage = async () => {
    console.log("Button clicked");

    const response = await fetch("http://127.0.0.1:8000/");

    console.log(response);

    const data = await response.json();

    console.log(data);

    setMessage(data.message);
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>PlacementIQ</h1>

      <button onClick={getMessage}>
        Connect Backend
      </button>

      <h2>{message}</h2>
    </div>
  );
}

export default App;