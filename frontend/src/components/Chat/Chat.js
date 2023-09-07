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

  //TODO: mMake a function like fetchChatHistory where it requests all the personalities from the database and adds them
  //currently when we access contacts, we just index at zero it seems.
  const [contacts, setContacts] = useState([
    { id: 1, name: 'Travel Agent', image: myImage, lastMessage: 'Hey there!' }, // Test Data
    // { id: 2, name: 'Jane Smith', image: myImage, lastMessage: 'See you tomorrow' },
  ]);
  const [chatHistory, setChatHistory] = useState([]);

  console.log('Chat component function is running');

  useEffect(() => {
    // Fetch contacts from the server and setContacts
    // TODO: provide which personality id to get conversation for. Assume that conversation exists in backend even if not talked to before.
    // Backend handles new covnersations
    const fetchChatHistory = async () => {
      console.log("trying to call api/fetch_chat_history");
      try {
        const response = await fetch('api/fetch_chat_history', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if(!response.ok) {
          throw new Error('HTTP error! status: ${response.status}');
        }
        const chatHistory = await response.json();
        setChatHistory(chatHistory);
      } catch (error) {
        console.error('Failed to fetch chat history: ', error);
      }
    };

    fetchChatHistory();
  }, []);

  //TODO: This is where the user clicks the contact. does not swap anything. Would have to update this function
  //Would have to fetch chat history and provide the correct chat ID
  // [1] update the message history that is displayed (would recall 'fetchChatHistory)
  // [2] update some state so when new message is sent, we get correct response
  // [3] should block changing contacts until we get response from last message? (another ticket)
  // dont want wrong personality to have response displayed
  // maybe when get response, and not on correct ID, dont display it. 
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
        content: newMessage,
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

    setIsTyping(false);

    setChatHistory(prevChatHistory => [
      ...prevChatHistory,
      {
        role: "assistant",
        content: data.content,
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