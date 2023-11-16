// components/InputSection.jsx

import React, {useState} from 'react';
import SendIcon from '@mui/icons-material/Send';

/**
 * InputSection component
 * @param {function} sendMessage - function to send message to backend
 * @param {boolean} disabled - whether or not to disable the input section
 * @return {JSX.Element}
 */
function InputSection({sendMessage, disabled}) {
  const [message, setMessage] = useState('');

  /**
   * Gets the number of lines in the text
   * @param {string} text - text to get number of lines of
   * @return {number} number of lines
   */
  const getNumberOfLines = (text) => {
    const maxLines = 6;
    const lines = text.split('\n').length;
    return Math.min(lines, maxLines);
  };

  /**
   * Handles key down events
   * If the user presses enter without shift, submit the message
   * @param {KeyboardEvent} e - key down event
   * @return {void}
   */
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Prevent adding a new line
      handleSubmit(e);
    }
  };

  /**
   * Handles submit events
   * If the message is not empty, send the message to the backend
   * @param {Event} e - submit event
   * @return {void}
   */
  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!message.trim()) return; // Don't send empty message

    sendMessage(message); // Send message to backend
    setMessage(''); // Clear text box for next question
  };

  return (
    <form className="input-form-section" onSubmit={(e) => handleSubmit(e)}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          flexGrow: 1,
        }}
      >
        <textarea
          rows={getNumberOfLines(message) || 1}
          className="form-input"
          value={message}
          onKeyDown={handleKeyDown}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
          disabled={disabled}
        />
      </div>
      <div
        className="send-icon"
        onClick={!disabled ? (e) => handleSubmit(e) : null}
      >
        <SendIcon />
      </div>
    </form>
  );
}

InputSection.propTypes = {
  sendMessage: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
};

export default InputSection;
