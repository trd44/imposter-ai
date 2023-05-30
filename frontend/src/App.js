// src/App.js
// import { Configuration, OpenAIApi } from 'openai';

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';

import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Home from './components/Home/Home';
import NavBar from './components/NavBar/NavBar';
import Chat from './components/Chat/Chat'

import FormSection from './components/Chat/InputSection';
import AnswerSection from './components/Chat/MessagesSection';
// import { makeStyles } from '@mui/system/make';
// import Paper from '@mui/material/Paper'
// import Grid from '@mui/material/Grid'
// import Box from '@mui/material/Box'
// import Divider from '@mui/material/Divider'
// import TextField from '@mui/material/TextField';
// import Typography from '@mui/material/Typography';
// import List from '@mui/material/List';
// import ListItem from '@mui/material/ListItem';
// import ListItemIcon from '@mui/material/ListItemIcon';
// import ListItemText from '@mui/material/ListItemText';
// import Avatar from '@mui/material/Avatar';
// import Fab from '@mui/material/Fab';
// import SendIcon from '@mui/icons-material/Send';

import "./App.css";

const App = () => {
  const [token, setToken] = useState();

  if (!token) {
    return (
      <Router>
        {/* <NavBar /> */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login setToken={setToken} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </Router>
    )
  }

  return (
    <Router>
      <Routes>
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </Router>
  );
};

  // const [token, setToken] = useState();
  // const [name, setName] = useState('');
  // const [message, setMessage] = useState('');
  // const [storedValues, setStoredValues] = useState([]);
  

  // const generateResponse = async (newQuestion, setNewQuestion) => {
  //   const response = await fetch('api/send_user_message', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify({ newQuestion }),
  //   });

  //   const data = await response.json();

  //   setStoredValues([
  //     {
  //       question: newQuestion,
  //       answer: data.content,
  //     },
  //     ...storedValues,
  //   ]);
  //   setNewQuestion('');
  // }

  // if(!token) {
  //   return <Login setToken={setToken} />
  // }

  // return (
  //   <div className='app-container'>
  //     <div className="header-section">
  //       <h1>Imposter.AI 🤖</h1>
  //       <p>
  //       This project is a work in progress that aims to use different System prompts 
  //       to teach ChatGPT how to behave in various roles, such as a travel agent.
  //       <br/>
  //       <br/>
  //       Click send or press enter to submit your message. We are working to add an indicator that Imposter is working on an answer.
  //       <br/>
  //       <br/>
  //       Start by saying Hello!
  //       </p>
  //     </div>
  //     <div className="content-wrapper">
  //       <div className="content-section">
  //         <AnswerSection storedValues={storedValues} />
  //       </div>
  //       <FormSection generateResponse={generateResponse} />
  //     </div>
  //     <Router>
  //     <Routes>
  //       <Route path="/login" element={<Login />} />
  //       <Route path="/register" element={<Register />} />
  //     </Routes>
  //   </Router>
  //   </div>

export default App;