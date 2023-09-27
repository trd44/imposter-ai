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

    return (
        <div className='messages-section'>
            {console.log(chatHistory)}
            {chatHistory.map((msg, index) => (
                <div
                    key={index}
                    /*
                    ** NOTE: 
                        - Here is where the message section partitions the conversation json
                        - Currently, system message is displayed
                    ** TODO: Remove system message from being displayed and display a separate first message!
                    */
                    className={`message-bubble ${msg.role === 'user' ? 'message-user' : 'message-assistant'}`}
                >
                    <p >{msg.content}</p>
                    {/* <div
                        className="copy-icon"
                        onClick={() => copyText(msg.message)}
                    >
                        <ContentCopyIcon />
                        <i className="fa-solid fa-copy"></i>
                    </div> */}
                </div>
            ))}
            <div ref={bottomRef}></div>
        </div>
    );
}

export default MessagesSection;