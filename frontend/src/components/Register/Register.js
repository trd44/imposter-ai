// src/components/Register/Register.js

import React, {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';

import './Register.css';

/**
 * Registers a user with the given credentials.
 * @param {object} credentials - The user's credentials.
 * @param {string} credentials.username - The user's username.
 * @param {string} credentials.password - The user's password.
 * @return {Promise<{
 *  response: Response, data: {token: string, token_expiry: string}
 * }>} - The response and data from the server.
 * @throws {Error} - An error occurred while registering in.
 */
async function registerUser(credentials) {
  try {
    const response = await fetch('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Registration failed: ${errorText || response.status}`);
    }

    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error(
          'Received unexpected content type from registration endpoint',
      );
    }

    const data = await response.json();
    return {response, data};
  } catch (error) {
    console.error('An error occurred while registering', error);
    throw error;
  }
}

/**
 * A registration form.
 * @param {object} props - The component props.
 * @param {function} props.setToken - A callback to be called after a successful
 * registration.
 * @param {function} props.setUsername - A callback to be called after a
 * successful registration.
 * @return {JSX.Element} - The element to render.
 */
export default function Register({setToken, setUsername}) {
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // Use the useNavigate hook to get access to the navigate function
  const navigate = useNavigate();

  /**
   * Handles the form submission.
   * @param {Event} e - The form submission event.
   * @return {void}
   * @throws {Error} - An error occurred while registering in.
   */
  const handleSubmit = async (e) => {
    // Prevent the default form action
    e.preventDefault();

    // Reset the error message
    setErrorMessage('');

    // If username or password is empty, set an error message and return early
    if (!username.trim() || !password.trim()) {
      setErrorMessage('Username and password are required');
      return;
    }

    // Try to register the user
    try {
      const {response, data} = await registerUser({
        username,
        password,
      });

      if (!response.ok) {
        setErrorMessage(data.error);
        return;
      }

      const {token, tokenExpiry} = data;
      setToken(token);
      localStorage.setItem('token', token);
      localStorage.setItem('tokenExpiry', tokenExpiry);

      setUsername(username);
      localStorage.setItem('username', username);

      navigate('/chat');
    } catch (error) {
      console.error('An error occurred while registering in', error);
      setErrorMessage(err.message);
    }
  };

  return (
    <div className="register-wrapper">
      <h1>Please Register</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input
            type="text"
            onChange={(e) => setUserName(e.target.value)}
          />
        </label>
        <label>
          <p>Password</p>
          <input
            type="password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
      <p>Already have an account? <Link to="/login">Login</Link></p>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
    </div>
  );
}

Register.propTypes = {
  setToken: PropTypes.func.isRequired,
  setUsername: PropTypes.func.isRequired,
};
