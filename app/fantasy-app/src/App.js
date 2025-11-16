import './App.css';
import { useState, useEffect } from 'react';
import { useRoutes } from "react-router-dom";
import FantasyTeam from './pages/FantasyTeam.js'
import { NavigationBar, PageFooter } from './pages/Main.js'
import LoginPage from './pages/Login.js'
import Transfers from './pages/Transfers.js'

export const api_network = "http:///192.168.1.60:8000"
export const local_api_network = "http://127.0.0.1:8000"

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return localStorage.getItem("isLoggedIn") === "true";
  });

  useEffect(() => {
    localStorage.setItem("isLoggedIn", isLoggedIn);
  }, [isLoggedIn]);

  const [userID, setUserID] = useState(() => {
    return localStorage.getItem("userID");
  })

  useEffect(() => {
    localStorage.setItem("userID", userID);
  }, [userID]);


  const routes = useRoutes([
    { path: "/", element: <MainPage isLoggedIn={isLoggedIn}/> },
    { path: "/team", element: 
      (isLoggedIn)
      ? <FantasyTeam userID={userID}/> 
      : <LoginPage 
      isLoggedIn={isLoggedIn} 
      setIsLoggedIn={setIsLoggedIn} 
      userID={userID} 
      setUserID={setUserID}/>},
    { path: "/login", element: <LoginPage 
      isLoggedIn={isLoggedIn} 
      setIsLoggedIn={setIsLoggedIn} 
      userID={userID} 
      setUserID={setUserID}/> },
    { path: "/transfers", element: 
      (isLoggedIn)
      ? <Transfers userID={userID}/> 
      : <LoginPage 
      isLoggedIn={isLoggedIn} 
      setIsLoggedIn={setIsLoggedIn} 
      userID={userID} 
      setUserID={setUserID}/>}
  ]);
  return (
    <>
      <NavigationBar/>
      {routes}
      <PageFooter/>
    </>
  );
}

function MainPage({ isLoggedIn }) {

  return (
    <div id="main-page">
      <main>
        <HomePage isLoggedIn={isLoggedIn}/>
      </main>
    </div>
  );
}

function HomePage({ isLoggedIn }) {
  return (
    <div id="home-page">
      <h2>Welcome to Fantasy NWSL!</h2>
      <p>Your ultimate destination for managing your fantasy NWSL team</p>
    </div>
  );
}

export default App;
