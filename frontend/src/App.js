// src/App.js

// Import necessary packages and components
import React, {useState, useEffect} from 'react';
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from 'react-router-dom';

import Chat from './components/Chat/Chat';
import Footer from './components/Footer/Footer';
import Home from './components/Home/Home';
import Login from './components/Login/Login';
import NavBar from './components/NavBar/NavBar';
import Register from './components/Register/Register';

import './App.css';

// Main App component
const App = () => {
  const [token, setToken] = useState();
  const initialUsername = localStorage.getItem('username') || '';
  const [username, setUsername] = useState(initialUsername);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    document.title = 'imposter.ai';

    const storedToken = localStorage.getItem('token');
    const tokenExpiryValue = localStorage.getItem('tokenExpiry');
    const storedTokenExpiry = Number(tokenExpiryValue) * 1000;

    if (storedToken && new Date().getTime() < storedTokenExpiry) {
      setToken(storedToken);
    } else {
      // If the token is expired, clear it from local storage
      localStorage.removeItem('token');
      localStorage.removeItem('tokenExpiry');
      localStorage.removeItem('username');
    }

    setLoading(false);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  const handleSuccessfulLogin = (token, tokenExpiry, username) => {
    setToken(token);
    localStorage.setItem('token', token);
    localStorage.setItem('tokenExpiry', tokenExpiry);
    setUsername(username);
    localStorage.setItem('username', username);
  };

  return (
    <div className="App">
      <Router>
        <NavBar
          token={token} setToken={setToken}
          username={username}
          setUsername={setUsername}
        />

        {!token ? (
          <Routes>
            <Route path="/" element={<Home token={token} />} />
            <Route
              path="/login"
              element={<Login onSuccessfulLogin={handleSuccessfulLogin} />}
            />
            <Route
              path="/register"
              element={
                <Register
                  setToken={setToken}
                  setUsername={setUsername}
                />}
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        ) : (
          <Routes>
            <Route path="/" element={<Home token={token} />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        )}
        <Footer />
      </Router>
    </div>
  );
};

export default App;
