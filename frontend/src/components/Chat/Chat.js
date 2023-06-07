// src/components/Chat/Chat.js

import React, { useState, useEffect } from 'react';

import InputSection from './InputSection';
import MessagesSection from './MessagesSection';
import ContactList from './ContactList';

import myImage from '../../TestContact.jpeg'; // adjust the path as needed


import './Chat.css';

export default function Chat() {
  const [contacts, setContacts] = useState([
    { id: 1, name: 'John Doe', image: myImage, lastMessage: 'Hey there!' },
    { id: 2, name: 'Jane Smith', image: myImage, lastMessage: 'See you tomorrow' },
  ]);

  useEffect(() => {
    // TODO: Fetch contacts from the server and setContacts
  }, []);

  const handleContactClick = (contactId) => {
    // TODO: Handle when a contact is clicked
    console.log(`Contact clicked: ${contactId}`);
  };

  const [token, setToken] = useState();
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [storedValues, setStoredValues] = useState([
    {
      role: "User",
      message: 'Hello!',
    },
    {
      role: "Assistant",
      message: "Hi, how can I help you?",
    },
    {
      role: "User",
      message: 'Hello!',
    },
    {
      role: "Assistant",
      message: "Hi, how can I help you?",
    },
    {
      role: "User",
      message: 'Hello!',
    },
    {
      role: "Assistant",
      message: "Hi, how can I help you?",
    },
    {
      role: "User",
      message: 'Hello!',
    },
    {
      role: "Assistant",
      message: "Hi, how can I help you?",
    }
  ]);

  const generateResponse = async (newQuestion, setNewQuestion) => {
    const response = await fetch('api/send_user_message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ newQuestion }),
    });

    const data = await response.json();

    setStoredValues(oldValues => [
      {
        question: newQuestion,
        answer: data.content,
      },
      ...oldValues,
    ]);
    setNewQuestion('');
  }

  return (
    <div className='chat-container'>
      <div className="contacts-section">
      <h1>Contacts</h1>
        <ContactList contacts={contacts} onContactClick={handleContactClick} />
      </div>
      <div className="chat-wrapper">
        <header>
          <h1>Travel Agent Imposter</h1>
          Click send or press enter to submit your message.
          <br />
          We are working to add an indicator that Imposter is working on an answer.
          <br />
          Start by saying Hello!
        </header>
        <div className="messages-section">
          <MessagesSection storedValues={storedValues} />
        </div>
        <InputSection generateResponse={generateResponse} />
      </div>
    </div>
  );
};