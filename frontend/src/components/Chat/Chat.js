// src/components/Chat/Chat.js

import React, { useState, useEffect } from 'react';

import InputSection from './InputSection';
import MessagesSection from './MessagesSection';
import ContactList from './ContactList';

import './Chat.css';

export default function Chat() {
  const [token, setToken] = useState();
  const [name, setName] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sendButtonEnabled, setSendButtonEnabled] = useState(true);
  const [activeContactId, setActiveContactId] = useState(0);
  const [menuOpen, setMenuOpen] = useState(false);

// Retreive an image from URL
const getImageUrl = (imageName) => {
    console.log('Fetching Image: ', imageName);
    return `/backend_assets/${imageName}`
  }

  const [contacts, setContacts] = useState([]);
  
  // Function to fetch contacts (personalities) from the database
  const fetchContacts = async () => {
    try {
      // Retrieve array of personalities for current user
      console.log("trying to call backend/fetch_contacts");
      const token = localStorage.getItem('token');
      const response = await fetch('backend/fetch_contacts', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      
      // Map through the data (array of contacts) to create the contact objects
      const fetchedContacts = data.map(contact => ({
        id: contact.id,
        name: contact.nickname,
        image: getImageUrl(contact.img),
        lastMessage: 'Hey there!', // TODO: replace with actual message data if availabe
      }));
  
      // Use setContacts to update the state
      setContacts(fetchedContacts);
      
    } catch (error) {
      console.error(`Failed to fetch contacts: ${error}`);
    }
  };
  
  // Call fetchContacts once when the component is mounted
  useEffect(() => {
    fetchContacts();
  }, []);
  

  const [chatHistory, setChatHistory] = useState([]);

  console.log('Chat component function is running');

  // Fetch contacts from the server and setContacts
  // TODO: provide which personality id to get conversation for. Assume that conversation exists in backend even if not talked to before.
  // Backend handles new covnersations [COMPLETED]
  const fetchChatHistory = async () => {
    console.log("trying to call api/fetch_chat_history");
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('api/fetch_chat_history', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          id: activeContactId
        })
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      console.log("retrieving new history for the contact: ", activeContactId)
      const chatHistory = await response.json();
      console.log("updating chat history given response!")
      setChatHistory(chatHistory);
    } catch (error) {
      console.error('Failed to fetch chat history: ', error);
    }
  };

  useEffect(() => {
    fetchChatHistory();
  }, [activeContactId]);

  // Select contact to have conversation with
  const handleContactClick = (contactId) => {

    // [1] Update active contact ID
    console.log(`Contact clicked: ${contactId}`);
    setActiveContactId(contactId);
    console.log('Updated Contact: ', activeContactId)
    // [2] Retrieve and display chat history for selected contact (will happen automatically)

    // [3] Transition UI for chatting with contact
    setMenuOpen(false); // Close the contacts menu
  };

  // Send message to backend and get response. Async, so user can continue to use UI
  const sendMessage = async (newMessage, activeContactId) => {

    // Ensure newMessage is not an empty string
    if (!newMessage.trim()) return;

    setSendButtonEnabled(false);
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
    //    * The fetch request below is a POST request to "/api/send_user_message"
    //    * The data sent is 'newMessage' which is assigned the value of whatever
    //    * the user has entered into the chat input field.
    const token = localStorage.getItem('token');
    const response = await fetch('api/send_user_message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ newMessage, activeContactId }), // Include the newMessage and ID in the body sent to the server
    });

    const data = await response.json();

    setIsTyping(false);
    setSendButtonEnabled(true);

    // Verify that response id matches the request ID, e.g. data.id == id
    // IFF response id matches active ID, update chat history (which will impact what is displayed to user)
    // ELSE: display nothing new
    if (data.id === activeContactId) {
      setChatHistory(prevChatHistory => [
        ...prevChatHistory,
        {
          role: "assistant",
          content: data.content,
        },

      ]);
    }

    // NOTE: Will not clear text box when receive response.
  }

  return (
    <div className='chat-container'>
      <div className="hamburger">
        <button onClick={() => setMenuOpen(!menuOpen)}>
          Contacts List
        </button>
      </div>
      <div className={`main-content ${menuOpen ? 'menu-open' : ''}`}>
        <div className={`contacts-section ${menuOpen ? 'open' : ''}`}>
          {/* <h2>Contacts</h2> */}
          <ContactList contacts={contacts} onContactClick={handleContactClick} />
        </div>

        <div className="chat-wrapper">
          <h2>{contacts.find(contact => contact.id === activeContactId)?.name || "Unknown"}</h2>
          Start by saying Hello!
          <div className="messages-section">
            <MessagesSection chatHistory={chatHistory} />
            {isTyping && <div className="message-bubble message-assistant">
              <p className="typing-text">Imposter is typing</p>
            </div>}


          </div>
          {/* The '0' is a placeholder for the message id
        TODO: replace the hardcoded ID with a state variable tracking ID */}
          <InputSection disabled={!sendButtonEnabled} sendMessage={(message) => sendMessage(message, activeContactId)} />
        </div>
      </div>
    </div>
  );
};