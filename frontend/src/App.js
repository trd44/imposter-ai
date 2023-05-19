// src/App.js
// import { Configuration, OpenAIApi } from 'openai';

import FormSection from './components/FormSection';
import AnswerSection from './components/AnswerSection';

import React, { useState, useEffect } from 'react';

// import { makeStyles } from '@mui/system/make';
import Paper from '@mui/material/Paper'
import Grid from '@mui/material/Grid'
import Box from '@mui/material/Box'
import Divider from '@mui/material/Divider'
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import Fab from '@mui/material/Fab';
import SendIcon from '@mui/icons-material/Send';

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

  // const { Configuration, OpenAIApi } = require("openai");

  // const configuration = new Configuration({
  //   apiKey: process.env.OPENAI_API_KEY,
  // });
  // const openai = new OpenAIApi(configuration);

  const [storedValues, setStoredValues] = useState([]);

  return (
    <div className='app-container'>
      <div className="header-section">
        <h1>Imposter.AI 🤖</h1>
        <p>
        This project is a work in progress that aims to use different System prompts 
        to teach ChatGPT how to behave in various roles, such as a travel agent.
        <br/>
        <br/>
        Click send or press enter to submit your message. We are working to add an indicator that Imposter is working on an answer.
        <br/>
        <br/>
        Start by saying Hello!
        </p>
      </div>
      <div className="content-wrapper">
        <div className="content-section">
          <AnswerSection storedValues={storedValues} />
        </div>
        <FormSection generateResponse={generateResponse} />
      </div>
    </div>
  );
};

export default App;