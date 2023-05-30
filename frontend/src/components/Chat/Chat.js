// src/components/Chat/Chat.js

import React, { useState, useEffect } from 'react';

import FormSection from '../FormSection';
import AnswerSection from '../AnswerSection';

export default function Chat() {
  const [token, setToken] = useState();
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [storedValues, setStoredValues] = useState([]);
  

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

//   if(!token) {
//     return <Login setToken={setToken} />
//   }

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