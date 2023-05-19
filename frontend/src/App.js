// import logo from './logo.svg';
// import './App.css';
// import React, { useEffect, useState } from 'react';
// import axios from 'axios'

// function App() {
//   const [getMessage, setGetMessage] = useState({})

//   useEffect(()=>{
//     axios.get('http://127.0.0.1:5000/flask/hello').then(response => {
//       console.log("SUCCESS", response)
//       setGetMessage(response)
//     }).catch(error => {
//       console.log(error)
//     })

//   }, [])
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>React + Flask Tutorial</p>
//         <div>{getMessage.status === 200 ? 
//           <h3>{getMessage.data.message}</h3>
//           :
//           <h3>LOADING</h3>}</div>
//       </header>
//     </div>
//   );
// }

// export default App;


// src/App.js
// import { Configuration, OpenAIApi } from 'openai';

import FormSection from './components/FormSection';
import AnswerSection from './components/AnswerSection';

import React, { useState, useEffect } from 'react';

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

  const [name, setName] = useState('');
  const [message, setMessage] = useState('');

  const generateResponse = async (newQuestion, setNewQuestion) => {
    const response = await fetch('api/send_user_message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ newQuestion }),
    });

    const data = await response.json();

    setStoredValues([
      {
        question: newQuestion,
        answer: data.content,
      },
      ...storedValues,
    ]);
    setNewQuestion('');
  }

  const { Configuration, OpenAIApi } = require("openai");

  const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
  });
  const openai = new OpenAIApi(configuration);

  const [storedValues, setStoredValues] = useState([]);
  useEffect(()=>{
    axios.get('https://imposter-ai.herokuapp.com/flask/hello').then(response => {
      console.log("SUCCESS", response)
      setGetMessage(response)
    }).catch(error => {
      console.log(error)
    })

  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>React + Flask Tutorials</p>
        <div>{getMessage.status === 200 ? 
          <h3>{getMessage.data.message}</h3>
          :
          <h3>LOADING</h3>}</div>
      </header>
    </div>
  );
}

export default App;