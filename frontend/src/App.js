// src/App.js

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Link, Routes, Navigate } from 'react-router-dom';

import Chat from './components/Chat/Chat'
import Footer from './components/Footer/Footer';
import Home from './components/Home/Home';
import Login from './components/Login/Login';
import NavBar from './components/NavBar/NavBar';
import Register from './components/Register/Register';

import "./App.css";

const App = () => {
  const [token, setToken] = useState();
  const [username, setUsername] = useState(localStorage.getItem('username') || '');

  // This effect runs once when the component mounts
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []); // The empty array means this effect runs once on mount and not on updates

  return (
    <div className="App">
      <Router>
      <NavBar token={token} setToken={setToken} username={username} setUsername={setUsername} />

        {!token ? (
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login setToken={setToken} setUsername={setUsername} />} />
            <Route path="/register" element={<Register setToken={setToken} setUsername={setUsername} />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        ) : (
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        )}
        <Footer />
      </Router>
    </div>
  )
};

export default App;