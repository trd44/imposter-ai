// src/components/Chat/Contact.js

import React from 'react';

/**
 * Contact component representing a single contact in the contacts list.
 * It displays the contact's name, profile picture, and last message preview.
 * It also handles user interaction by calling the onClick callback when
 * clicked.
 * @return {React.Component} The Contact component UI.
 */
function Contact({contact, onClick}) {
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

Contact.propTypes = {
  contact: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    image: PropTypes.string.isRequired,
    lastMessage: PropTypes.string.isRequired,
  }).isRequired,
  onClick: PropTypes.func.isRequired,
};

export default Contact;
