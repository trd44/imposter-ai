// components/MessagesSection.jsx
import React, { useEffect, useRef } from 'react';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';


const MessagesSection = ({ chatHistory }) => {
    const copyText = (text) => {
        navigator.clipboard.writeText(text);
    };

    const bottomRef = useRef(null);

    useEffect(() => {
        if (bottomRef.current) {
            bottomRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [chatHistory]);

    // Filter out system messages
    const filteredChatHistory = chatHistory.filter((msg) => msg.role !== 'system');

    return (
        <div className='messages-section'>
            {console.log(chatHistory)}
            {filteredChatHistory.map((msg, index) => (
                <div
                    key={index}
                    className={`message-bubble ${msg.role === 'user' ? 'message-user' : 'message-assistant'}`}
                >
                    <p >{msg.content}</p>
                </div>
            ))}
            <div ref={bottomRef}></div>
        </div>
    );
}

export default MessagesSection;