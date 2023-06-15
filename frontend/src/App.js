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
  // State for storing user token
  const [token, setToken] = useState();

  // State for storing username, initialised with username from local storage if it exists
  const [username, setUsername] = useState(localStorage.getItem('username') || '');

  // This effect runs once when the component mounts
  useEffect(() => {
    // Check if a user token is stored in local storage
    const storedToken = localStorage.getItem('token');

    // If a stored token exists, set it as the current token state
    if (storedToken) {
      setToken(storedToken);
    }
  }, []); // This effect runs once on mount and not on updates  

  return (
    <div className="App">
      <Router>
        {/* Pass token and username states to NavBar */}
        <NavBar token={token} setToken={setToken} username={username} setUsername={setUsername} />

        {/* If user is not authenticated, only show login and register routes */}
        {/* If user is authenticated, show chat route in addition to home */}
        {!token ? (
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login setToken={setToken} setUsername={setUsername} />} />
            <Route path="/register" element={<Register setToken={setToken} setUsername={setUsername} />} />
            {/* If any other path is visited, redirect to home */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        ) : (
          <Routes>
            <Route path="/" element={<Home />} />
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