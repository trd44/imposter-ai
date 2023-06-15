// src/components/Register/Register.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import './Register.css';

async function registerUser(credentials) {
  const response = await fetch('/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })

  const data = await response.json();
  return { response, data };
}


export default function Register({ setToken, setUsername }) {
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
      const { response, data } = await registerUser({
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
      setUsername(username)
      localStorage.setItem('username', username);
      navigate("/chat")
    } catch (err) {
      console.error("An error occurred while registering in", err);
      setErrorMessage(err.message);
    }
  }

  return (
    <div className="register-wrapper">
      <h1>Please Register</h1>
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