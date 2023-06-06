// src/components/Chat/Contact.js

import React from 'react';

function Contact({ contact, onClick }) {
    return (
      <div className="contact" onClick={onClick}>
        <img className="contact-image" src={contact.image} alt={contact.name} />
        <div className="contact-info">
          <div className="contact-name">{contact.name}</div>
          <div className="contact-last-message">{contact.lastMessage}</div>
        </div>
      </div>
    );
  }

export default Contact;
