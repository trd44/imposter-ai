// src/components/Login/Login.js

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

import './Login.css';

// Calls the login function on the server
async function loginUser(credentials) {
  const response = await fetch('/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })

  const data = await response.json();
  return { response, data };
}


export default function Login({ setToken, setUsername }) {
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();

    setErrorMessage('');

    if (!username.trim() || !password.trim()) {
      setErrorMessage('Username and password are required');
      return;
    }

    try {
      const { response, data } = await loginUser({
        username,
        password
      });

      if (!response.ok) {
        setErrorMessage(data.error);
        return;
      }

      const { token } = data;
      setToken(token);
      localStorage.setItem('token', token);
      setUsername(username);
      localStorage.setItem('username', username);
      navigate("/chat");
    } catch (err) {
      console.error("An error occurred while logging in", err);
      setErrorMessage(err.message);
    }
  }

  return (
    <div className="login-wrapper">
      <h1>Please Log In</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input
            type="text"
            onChange={e => setUserName(e.target.value)}
          />
        </label>
        <label>
          <p>Password</p>
          <input
            type="password"
            onChange={e => setPassword(e.target.value)}
          />
        </label>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
    </div>
  )
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
}