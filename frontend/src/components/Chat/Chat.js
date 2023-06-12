// src/components/Chat/Chat.js

import React, { useState, useEffect } from 'react';

import InputSection from './InputSection';
import MessagesSection from './MessagesSection';
import ContactList from './ContactList';

import myImage from '../../TestContact.jpeg'; // adjust the path as needed


import './Chat.css';

export default function Chat() {
  const [token, setToken] = useState();
  const [name, setName] = useState('');
  const [newMessage, setNewMessage] = useState('');
  const [contacts, setContacts] = useState([
    { id: 1, name: 'John Doe', image: myImage, lastMessage: 'Hey there!' }, // Test Data
    { id: 2, name: 'Jane Smith', image: myImage, lastMessage: 'See you tomorrow' },
  ]);
  const [chatHistory, setChatHistory] = useState([
    {
      role: "user", // Test Data
      message: 'Hello!',
    },
    {
      role: "assistant",
      message: "Hi, how can I help you?",
    },
    {
      role: "user",
      message: 'Hello!',
    },
    {
      role: "assistant",
      message: "Hi, how can I help you?",
    },
    {
      role: "user",
      message: 'Hello!',
    },
    {
      role: "assistant",
      message: "Hi, how can I help you?",
    },
    {
      role: "user",
      message: 'Hello!',
    },
    {
      role: "assistant",
      message: "Hi, how can I help you?",
    }
  ]);

  useEffect(() => {
    // TODO: Fetch contacts from the server and setContacts
  }, []);

  const handleContactClick = (contactId) => {
    // TODO: Handle when a contact is clicked
    console.log(`Contact clicked: ${contactId}`);
  };

  const sendMessage = async (newMessage) => {

    // Ensure newMessage is not an empty string
    if(!newMessage.trim()) return;

    // Update the chat history with the User's newest message
    setChatHistory(prevChatHistory => {
      const updatedChatHistory =  [...prevChatHistory,
      {
        role: "user",
        message: newMessage,
      },
      
    ];
      console.log(updatedChatHistory);
      return updatedChatHistory;
  });

    // Call the send_user_message function on the backend
    const response = await fetch('api/send_user_message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ newMessage }),
    });

    const data = await response.json();

    setChatHistory(prevChatHistory => [
      ...prevChatHistory,
      {
        role: "assistant",
        message: data.content,
      },
      
    ]);
    setNewMessage('');
  }

  return (
    <div className='chat-container'>
      <div className="contacts-section">
      <h2>Contacts</h2>
        <ContactList contacts={contacts} onContactClick={handleContactClick} />
      </div>
      <div className="chat-wrapper">
        {/* <header> */}
          <h2>Travel Agent Imposter</h2>
          We are working to add an indicator that Imposter is working on an answer.
          <br />
          Start by saying Hello!
        {/* </header> */}
        <div className="messages-section">
          <MessagesSection chatHistory={chatHistory} />
        </div>
        <InputSection sendMessage={sendMessage} />
      </div>
    </div>
  );
};