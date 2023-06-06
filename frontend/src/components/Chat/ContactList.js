// src/components/Chat/ContactList.js

import React from 'react';
import Contact from './Contact';

function ContactList({ contacts, onContactClick }) {
  return (
    <div className='contact-list'>
      {contacts.map((contact) => (
        <Contact 
          key={contact.id} 
          contact={contact}
          onClick={() => onContactClick(contact.id)} 
        />
      ))}
    </div>
  );
}

export default ContactList;
