// src/components/Login/Login.js

import React, {useState} from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {useNavigate} from 'react-router-dom';

import './Login.css';

/**
 * Logs in a user with the given credentials.
 * @param {object} credentials - The user's credentials.
 * @param {string} credentials.username - The user's username.
 * @param {string} credentials.password - The user's password.
 * @return {Promise<{
 *   response: Response, data: {token: string, token_expiry: string}
 * }>} - The response and data from the server.
 * @throws {Error} - An error occurred while logging in.
 * @throws {TypeError} - The response was not JSON.
 * @throws {Error} - The response was not ok.
 */
async function loginUser(credentials) {
  try {
    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      throw new Error(`Login failed with status: ${response.status}`);
    }

    const contentType = response.headers.get('content-type');

    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();
      return {response, data};
    } else {
      const text = await response.text();
      throw new Error(`Expected a JSON response, but got: ${text}`);
    }
  } catch (error) {
    console.error('An error occurred while logging in', error);
    throw error;
  }
}

/**
 * A login form.
 * @param {object} props - The component props.
 * @param {function} props.onSuccessfulLogin - A callback to be called after a
 * successful login.
 * @return {JSX.Element} - The element to render.
 */
export default function Login({onSuccessfulLogin}) {
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // Used to navigate to a new page after a successful login.
  const navigate = useNavigate();

  /**
   * Handles the form submission.
   * @param {Event} e - The form submission event.
   * @return {void}
   * @throws {Error} - An error occurred while logging in.
   * @throws {TypeError} - The response was not JSON.
   * @throws {Error} - The response was not ok.
   * @throws {Error} - Username and password are required.
   */
  const handleSubmit = async (e) => {
    // Prevent the browser from reloading the page.
    e.preventDefault();
    // Clear any previous error messages.
    setErrorMessage('');

    if (!username.trim() || !password.trim()) {
      setErrorMessage('Username and password are required');
      return;
    }

    try {
      const {response, data} = await loginUser({
        username,
        password,
      });

      if (!response.ok) {
        setErrorMessage(data.error);
        return;
      }

      const {token, tokenExpiry} = data;

      onSuccessfulLogin(token, tokenExpiry, username);
      navigate('/chat');
    } catch (err) {
      console.error('An error occurred while logging in', err);
      setErrorMessage(err.message);
    }
  };

  return (
    <div className="login-wrapper">
      <h1>Please Log In</h1>
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
      <p>Don&apos;t have an account? <Link to="/register">Register</Link></p>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
    </div>
  );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired,
  onSuccessfulLogin: PropTypes.func.isRequired,
};
