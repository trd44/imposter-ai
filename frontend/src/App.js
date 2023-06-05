// src/App.js

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';

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

  return (
    <div className="App">
      <Router>
        <NavBar token={token} username={username} />

        {!token ? (
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login setToken={setToken} />} />
            <Route path="/register" element={<Register />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        ) : (
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        )}
        <Footer />
      </Router>
    </div>
  )
};

export default App;