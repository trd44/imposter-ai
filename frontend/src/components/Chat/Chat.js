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

  // Fetch contacts when component mounts
  useEffect(() => {
    fetchContacts();
  }, []);

  // Fetch chat history when active contact changes
  useEffect(() => {
    fetchChatHistory();
  }, [activeContactId]);

  /**
   * Fetches contacts from the backend and updates the contacts state.
   */
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
        image: getContactPhotoURL(contact.img),
        lastMessage: contact.last_message, // TODO: replace with actual message
      }));

      setContacts(fetchedContacts);
    } catch (error) {
      console.error(`Failed to fetch contacts: ${error}`);
    }
  };

  /**
   * Returns the URL for a contact's photo.
   * @param {string} imageName The name of the image.
   * @return {string} The URL of the image.
   */
  const getContactPhotoURL = (imageName) => {
    return `/backend_assets/${imageName}`;
  };

  /**
   * Fetches chat history for the active contact from the backend and updates
   * the chat history state.
   */
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

  /**
   * Handles a contact being clicked by the user. Updates the active contact ID
   * and closes the contacts list menu.
   * @param {number} contactId The ID of the contact that was clicked.
   * @return {void}
   */
  const handleContactClick = (contactId) => {
    setActiveContactId(contactId);
    setMenuOpen(false);
  };

  /**
   * Sends a new message to the active contact and updates the chat history
   * state.
   * @param {string} newMessage The new message to send.
   * @param {number} activeContactId The ID of the active contact.
   * @return {void}
   * TODO: Add error handling
   */
  const sendMessage = async (newMessage, activeContactId) => {
    // If new message is empty, do nothing
    if (!newMessage.trim()) return;

    setSendButtonEnabled(false);
    setIsTyping(true);

    // Add new message to chat history (Which will display immediately)
    setChatHistory((prevChatHistory) => [...prevChatHistory, {
      role: 'user',
      content: newMessage,
    }]);

    try {
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

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (!data || typeof data !== 'object' || !data.content) {
        throw new Error('Invalid response format');
      }

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
      // Update the 'last message' for the contact where the response was
      // receieved
      const updatedContacts = contacts.map((contact) =>
        contact.id === data.id ? {...contact, lastMessage: data.content} :
        contact);
      setContacts(updatedContacts);
    } catch (error) {
      console.error('Failed to send message: ', error);
      // Handle UI updates or notifications for error feedback
      // Might want to remove the optimistic message addition
      // if we can determine that the message definitely failed to send
    } finally {
      setIsTyping(false);
      setSendButtonEnabled(true);
    }
  };

  // When to re-update the last message received in the contact list?...
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
                &nbsp;is typing
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
