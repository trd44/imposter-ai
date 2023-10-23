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

  // This effect runs once when the component mounts
  useEffect(() => {
    // Check if a user token is stored in local storage
    const storedToken = localStorage.getItem('token');
    const storedTokenExpiry = Number(localStorage.getItem('tokenExpiry')) * 1000; // Convert to milliseconds

    // If the stored token exists and it hasn't expired, set it as the current token state
    if (storedToken && new Date().getTime() < storedTokenExpiry) {
      setToken(storedToken);
    } else {
      // If the token is expired, clear it from local storage
      localStorage.removeItem('token');
      localStorage.removeItem('tokenExpiry');
      localStorage.removeItem('username');
    }

    setLoading(false); // Set loading to false after checking for token
  }, []); // This effect runs once on mount and not on updates  

  if (loading) {
    return <div>Loading...</div>; // Replace with your actual loading component or spinner
  }

  const handleSuccessfulLogin = (token, tokenExpiry, username) => {
    setToken(token);
    localStorage.setItem('token', token);
    localStorage.setItem('tokenExpiry', tokenExpiry);
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
            <Route path="/" element={<Home token={token} />} />
            <Route path="/login" element={<Login onSuccessfulLogin={handleSuccessfulLogin} />} />
            <Route path="/register" element={<Register setToken={setToken} setUsername={setUsername} />} />
            {/* If any other path is visited, redirect to home */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        ) : (
          <Routes>
            <Route path="/" element={<Home token={token} />} />
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