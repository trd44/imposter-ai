// src/components/Chat/Chat.js

import React, { useState, useEffect } from 'react';

import FormSection from './InputSection';
import AnswerSection from './MessagesSection';
import NavBar from '../NavBar/NavBar';
import Footer from '../Footer/Footer';

import './Chat.css';

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
    <div className='chat-container'>
      <NavBar />
      <header>
        <h1>Travel Agent Imposter</h1>
        Click send or press enter to submit your message.
        <br />
        We are working to add an indicator that Imposter is working on an answer.
        <br />
        Start by saying Hello!
      </header>
      <div className="chat-wrapper">
        <div className="messages-section">
          <AnswerSection storedValues={storedValues} />
        </div>
        <FormSection generateResponse={generateResponse} />
      </div>
      <Footer />
    </div>
  );
};