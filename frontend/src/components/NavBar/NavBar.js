// src/components/NavBar/NavBar.js

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './NavBar.css';

const NavBar = ({ token, setToken, username, setUsername }) => {
  const navigate = useNavigate();

  const logout = async () => {
    const response = await fetch('/auth/logout', {method: 'POST'})
    const data = await response.json();
    if (data.message === 'User logged out'){
      // Log the user out on the frontend by setting token and username to null
      setToken(null);
      setUsername(null);
      localStorage.removeItem('token');
      localStorage.removeItem('username');

      // Navigate the user to the home page
      navigate('/')
    } else {
      console.error('Error logging out')
    }
  }

  return (
    <nav className="navbar">
      <Link to="/" className="home-link">
        <h1>imposter.ai 🤖</h1>
      </Link>

      {!token ? (
        <div className="nav-links">
          <Link to="/register">Register</Link>
          <Link to="/login">Login</Link>
        </div>
      ) : (
        <div className="nav-links">
          Hi {username}!
          <Link onClick={logout}>Logout</Link>
        </div>
      )}
    </nav>
  );
};

export default NavBar;
