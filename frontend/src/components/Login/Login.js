import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import Register from "../Register/Register"

import './Login.css';

async function loginUser(credentials) {
    const response = await fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    })
    
    const data = await response.json();
    // return both response and data
    return { response, data };
}


export default function Login({ setToken }) {
    const [username, setUserName] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

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
                // Set the error message to the custom error returned from the backend
                setErrorMessage(data.error);
                return;
            }

            const { token } = data;
            setToken(token);
        } catch (err) {
            // An error occurred while trying to send the request
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
            <Router>
                <Link to="/register">Register</Link>
            </Router>
            </form>       
            {errorMessage && <p className="error-message">{errorMessage}</p>}
        </div>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
}