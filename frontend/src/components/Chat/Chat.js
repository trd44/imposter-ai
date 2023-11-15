// src/components/Chat/Chat.js

import React, {useState, useEffect} from 'react';

import InputSection from './InputSection';
import MessagesSection from './MessagesSection';
import ContactList from './ContactList';

import './Chat.css';

/**
 * Chat component representing the main chat interface of the application.
 * It handles displaying and managing chat conversations, contacts, and the
 * input section for sending new messages. This component fetches and displays
 * chat history for the active contact and updates it based on user interaction.
 * It also manages the contacts list and handles user actions like selecting a
 * contact to chat with or sending new messages.
 *
 * @return {React.Component} The Chat component UI.
 */
export default function Chat() {
  const [activeContactId, setActiveContactId] = useState(0);
  const [chatHistory, setChatHistory] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [sendButtonEnabled, setSendButtonEnabled] = useState(true);

  useEffect(() => {
    fetchContacts();
  }, []);

  useEffect(() => {
    fetchChatHistory();
  }, [activeContactId]);

  const fetchContacts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('backend/fetch_contacts', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Error fetching contacts. status: ${response.status}`);
      }

      const data = await response.json();

      const fetchedContacts = data.map((contact) => ({
        id: contact.id,
        name: contact.nickname,
        image: getContactPhoto(contact.img),
        lastMessage: 'Hey there!', // TODO: replace with actual message
      }));

      setContacts(fetchedContacts);
    } catch (error) {
      console.error(`Failed to fetch contacts: ${error}`);
    }
  };

  const getContactPhoto = (imageName) => {
    console.log('Fetching Image: ', imageName);
    return '/backend_assets/${imageName}';
  };

  const fetchChatHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('api/fetch_chat_history', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          id: activeContactId,
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const chatHistory = await response.json();
      setChatHistory(chatHistory);
    } catch (error) {
      console.error('Failed to fetch chat history: ', error);
    }
  };

  // When a contact is clicked, update the active contact ID
  const handleContactClick = (contactId) => {
    setActiveContactId(contactId);
    setMenuOpen(false);
  };

  // Send message to the backend and receive response
  const sendMessage = async (newMessage, activeContactId) => {
    // If new message is empty, do nothing
    if (!newMessage.trim()) return;

    setSendButtonEnabled(false);
    setIsTyping(true);

    // Add the new message to the chat history immediately
    setChatHistory((prevChatHistory) => {
      const updatedChatHistory = [...prevChatHistory,
        {
          role: 'user',
          content: newMessage,
        },
      ];

      return updatedChatHistory;
    });

    const token = localStorage.getItem('token');
    const response = await fetch('api/send_user_message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        newMessage,
        activeContactId,
      }),
    });

    const data = await response.json();

    setIsTyping(false);
    setSendButtonEnabled(true);

    // Verify that response id matches the activeContactId
    if (data.id === activeContactId) {
      // Update chat history (which will impact what is displayed to user)
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        {
          role: 'assistant',
          content: data.content,
        },
      ]);
    } else {
      console.error('Response ID does not match active contact ID');
    }
  };

  return (
    <div className='chat-container'>
      <div className="hamburger">
        <button onClick={() => setMenuOpen(!menuOpen)}>
          Contacts List
        </button>
      </div>
      <div className={`main-content ${menuOpen ? 'menu-open' : ''}`}>
        <div className={`contacts-section ${menuOpen ? 'open' : ''}`}>
          <ContactList
            contacts={contacts}
            onContactClick={handleContactClick}
          />
        </div>

        <div className="chat-wrapper">
          <h2>
            {contacts.find(
                (contact) => contact.id === activeContactId,
            )?.name || 'Unknown'}
          </h2>
          <div className="messages-section">
            <MessagesSection chatHistory={chatHistory} />
            {isTyping && <div className="message-bubble message-assistant">
              <p
                className="typing-text">{
                  contacts.find(
                      (contact) => contact.id === activeContactId,
                  )?.name || 'Unknown'
                }
                is typing
              </p>
            </div>}


          </div>
          <InputSection
            disabled={!sendButtonEnabled}
            sendMessage={(message) => sendMessage(message, activeContactId)}
          />
        </div>
      </div>
    </div>
  );
};
