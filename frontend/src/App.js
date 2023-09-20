// src/App.js

// Import necessary packages and components
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

import Chat from './components/Chat/Chat'
import Footer from './components/Footer/Footer';
import Home from './components/Home/Home';
import Login from './components/Login/Login';
import NavBar from './components/NavBar/NavBar';
import Register from './components/Register/Register';

import "./App.css";

// Main App component
const App = () => {
  const [loading, setLoading] = useState(true);
  // State for storing user token
  const [token, setToken] = useState();

  // State for storing username, initialised with username from local storage if it exists
  const [username, setUsername] = useState(localStorage.getItem('username') || '');

  useEffect(() => {
    document.title = "imposter.ai";
  }, []);

  // useEffect(() => {
  //   const link = document.querySelector("link[rel*='icon']") || document.createElement('link');
  //   link.type = 'image/x-icon';
  //   link.rel = 'shortcut icon';
  //   link.href = '%PUBLIC_URL%/favicon.ico';
    
  //   document.getElementsByTagName('head')[0].appendChild(link);
  // }, []);

  // This effect runs once when the component mounts
  useEffect(() => {
    // Check if a user token is stored in local storage
    const storedToken = localStorage.getItem('token');

    // If a stored token exists, set it as the current token state
    if (storedToken) {
      setToken(storedToken);
    }
    setLoading(false); // Set loading to false after checking for token
  }, []); // This effect runs once on mount and not on updates  

  if (loading) {
    return <div>Loading...</div>; // Replace with your actual loading component or spinner
  }
  const handleSuccessfulLogin = (token, username) => {
    setToken(token);
    localStorage.setItem('token', token);
    setUsername(username);
    localStorage.setItem('username', username);
  }

  return (
    <div className="App">
      <Router>
        {/* Pass token and username states to NavBar */}
        <NavBar token={token} setToken={setToken} username={username} setUsername={setUsername} />

        {/* If user is not authenticated, only show login and register routes */}
        {/* If user is authenticated, show chat route in addition to home */}
        {!token ? (
          <Routes>
            <Route path="/" element={<Home token={token}/>} />
            <Route path="/login" element={<Login onSuccessfulLogin={handleSuccessfulLogin} />} />
            <Route path="/register" element={<Register setToken={setToken} setUsername={setUsername} />} />
            {/* If any other path is visited, redirect to home */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        ) : (
          <Routes>
            <Route path="/" element={<Home token={token}/>} />
            <Route path="/chat" element={<Chat />} />
            {/* If any other path is visited, redirect to home */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        )}
        {/* Display Footer on all pages */}
        <Footer />
      </Router>
    </div>
  )
};

export default App;