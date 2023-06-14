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
  const [isTyping, setIsTyping] = useState(false);
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
    if (!newMessage.trim()) return;

    setIsTyping(true);

    // Update the chat history with the User's newest message
    setChatHistory(prevChatHistory => {
      const updatedChatHistory = [...prevChatHistory,
      {
        role: "user",
        message: newMessage,
      },

      ];
      console.log(updatedChatHistory);
      return updatedChatHistory;
    });

    // Call the send_user_message function on the backend
    const response = await fetch('api/old/send_user_message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ newMessage }),
    });

    const data = await response.json();

    setIsTyping(false);

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
        <h2>Travel Agent Imposter</h2>
        Start by saying Hello!
        <div className="messages-section">
          <MessagesSection chatHistory={chatHistory} />
          {isTyping && <div className="message-bubble message-assistant">
            <p className="typing-text">Imposter is typing</p>
          </div>}


        </div>
        <InputSection sendMessage={sendMessage} />
      </div>
    </div>
  );
};