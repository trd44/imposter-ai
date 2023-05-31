// // src/components/NavBar/NavBar.js

import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css';

const NavBar = ({ token, username }) => {

  // const username = localStorage.getItem('username');

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
          <Link to="/logout">Logout</Link>
        </div>
      )}
    </nav>
  );
};

export default NavBar;
