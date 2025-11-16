import { useState } from 'react'
import { api_network, local_api_network } from '../App';


function LoginPage({ isLoggedIn, setIsLoggedIn, userID, setUserID }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("")

  function handleSubmit(e) {
    e.preventDefault();
    handleLogin(username, password);
  }

  async function handleLogin(username, password){
    try {
      const response = await fetch(api_network + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data.message);
        setTimeout(() => setUserID(data.userID), 0);
        setIsLoggedIn(true); // this should set isLoggedIn for all pages
        setMessage(data.message);
        setUsername("");
        setPassword("");
        setError("");
      } else {
        const err = await response.json();
        setError(err.detail || "Login failed");
        setMessage("Login failed");
        console.error("Login failed:", error);
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Network error");
    }
  }

  function handleLogout(){
    // Clear login state and any stored data
    setIsLoggedIn(false);
    setUserID(null);
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("username");
    
  }

  return (
    <div id="login-page">
      {isLoggedIn ? (
        <>
        <p>You are logged in.</p>
        <button onClick={handleLogout}>Log Out</button>
        </>
      ) : (   
      <>  
      <h2>Login</h2>
      <form id="login-form" onSubmit={(e) => { handleSubmit(e);}}>
        <label htmlFor="username">Username:</label>
        <input type="text" id="username" name="username" required value={username} onChange={(e) => setUsername(e.target.value)}/>
        <br />
        <label htmlFor="password">Password:</label>
        <input type="password" id="password" name="password" required value={password} onChange={(e) => setPassword(e.target.value)}/>
        <br />
        <button type="submit">Login</button>
      </form>
      </>
      )}
      {message && (
        <p
          style={{
            color: responseColor(message),
            marginTop: "1rem",
            fontWeight: "bold",
          }}
        >
          {message}
        </p>
      )}
    </div>
  );
}

function responseColor(message) {
  if (message.toLowerCase().includes("success")) return "green";
  if (message.toLowerCase().includes("error")) return "red";
  if (message.toLowerCase().includes("invalid")) return "red";
  return "orange";
}

export default LoginPage;