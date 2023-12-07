// src/components/Chat/ContactList.js

import React from 'react';
import Contact from './Contact';

/**
 * ContactList component representing the list of contacts.
 * It displays a list of Contact components.
 * @return {React.Component} The ContactList component UI.
 */
function ContactList({contacts, onContactClick}) {
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

ContactList.propTypes = {
  contacts: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        image: PropTypes.string.isRequired,
        lastMessage: PropTypes.string.isRequired,
      }),
  ).isRequired,
  onContactClick: PropTypes.func.isRequired,
};

export default ContactList;
