import './App.css';
import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useRoutes } from "react-router-dom";
import TeamForm from './pages/FantasyTeam.js'
import { NavigationBar, PageFooter, PageHeader } from './pages/Main.js'
import LoginPage from './pages/Login.js'


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return localStorage.getItem("isLoggedIn") === "true";
  });

  useEffect(() => {
    localStorage.setItem("isLoggedIn", isLoggedIn);
  }, [isLoggedIn]);


  const routes = useRoutes([
    { path: "/", element: <MainPage isLoggedIn={isLoggedIn}/> },
    { path: "/team", element: <TeamForm isLoggedIn={isLoggedIn}/> },
    { path: "/login", element: <LoginPage isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} /> },
  ]);
  return routes;
}

function ProtectedRoute({ isLoggedIn, children }) {
  return isLoggedIn ? children : <Navigate to="/login" />;
}

function SaveButton() {
  const [save, setSave] = useState(false);

  function handleSave(){
    setSave(true);
  }

  return (
    <button save={save} onClick={handleSave}>{save ? "Saved" : "Save"}</button>
  );
}

function MainPage(isLoggedIn) {

  return (
    <div id="main-page">
      <NavigationBar/>
      <main>
        <HomePage isLoggedIn={isLoggedIn}/>
      </main>
      <PageFooter/>
    </div>
  );
}

function HomePage(isLoggedIn) {
  return (
    <div id="home-page">
      <h2>Welcome to Fantasy NWSL!</h2>
      <p>Your ultimate destination for managing your fantasy NWSL team</p>
    </div>
  );
}

export default App;
