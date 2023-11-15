// components/MessagesSection.jsx

import React, {useEffect, useRef} from 'react';

/**
 * MessagesSection
 * @param {Object[]} chatHistory - chat history
 * @param {string} chatHistory[].role - role of the message sender
 * @param {string} chatHistory[].content - content of the message
 * @return {JSX.Element}
 */
const MessagesSection = ({chatHistory}) => {
  const bottomRef = useRef(null);

  // Scroll to bottom of chat history when chat history changes
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({behavior: 'smooth'});
    }
  }, [chatHistory]);

  // Filter out system messages
  const filteredChatHistory = chatHistory.filter(
      (msg) => msg.role !== 'system',
  );

  return (
    <div className='messages-section'>
      {console.log(chatHistory)}
      {filteredChatHistory.map((msg, index) => (
        <div
          key={index}
          className={`message-bubble ${
            msg.role === 'user' ? 'message-user' : 'message-assistant'
          }`}
        >
          <p >{msg.content}</p>
        </div>
      ))}
      <div ref={bottomRef}></div>
    </div>
  );
};

MessagesSection.propTypes = {
  chatHistory: PropTypes.array,
};

export default MessagesSection;
