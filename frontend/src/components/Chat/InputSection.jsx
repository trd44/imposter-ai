// components/InputSection.jsx

import { useState, useRef, useEffect } from "react";
import SendIcon from '@mui/icons-material/Send';

function InputSection({ sendMessage, disabled }) {
  const [message, setMessage] = useState('');

  const getNumberOfLines = (text) => {
    const maxLines = 6;
    const lines = text.split('\n').length;
    return Math.min(lines, maxLines);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Prevent adding a new line
      handleSubmit(e);
    }
  };

  const handleSubmit = e => {
    if(e) e.preventDefault();
    if(!message.trim()) { // check if message is not empty or only contains whitespace
      return;
    }
    sendMessage(message);
    setMessage('');
  };

  return (
    <form className="input-form-section" onSubmit={(e) => handleSubmit(e)}>
      <div style={{ display: 'flex', justifyContent: 'space-between', flexGrow: 1 }}>
        <textarea
          // style={{ marginRight: '10px' }}
          rows={getNumberOfLines(message) || 1}
          className="form-input"
          value={message}
          // onInput={handleInput}
          onKeyDown={handleKeyDown}
          onChange={e => setMessage(e.target.value)}
          placeholder="Type a message..."
          disabled={disabled}
        />
      </div>
      <div
        className="send-icon"
        onClick={!disabled ? (e) => handleSubmit(e) : null}  // Disable onClick if disabled
      >
        <SendIcon />
      </div>
    </form>
  );
}

export default InputSection;