// components/MessagesSection.jsx
import React, { useEffect, useRef } from 'react';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';


const MessagesSection = ({ storedValues }) => {
    const copyText = (text) => {
        navigator.clipboard.writeText(text);
    };

    const bottomRef = useRef(null);

    useEffect(() => {
        if (bottomRef.current) {
            bottomRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [storedValues]);

    return (
        <div className='messages-section'>
          {storedValues.map((msg, index) => (
            <div 
              key={index}
              className={`message-bubble ${msg.role === 'User' ? 'message-user' : 'message-assistant'}`}
            >
              <p>{msg.message}</p>
            </div>
          ))}
        </div>
      );

    // return (
    //     <>
    //         <hr className="hr-line" />
    //         <div className="messages-section">
    //             {[...storedValues].reverse().map((value, index) => {
    //                 return (
    //                     <div className="answer-section" key={index}>
    //                         <p className="question">{value.question}</p>
    //                         <p className="answer">{value.answer}</p>
    //                         <div
    //                             className="copy-icon"
    //                             onClick={() => copyText(value.answer)}
    //                         >
    //                             <ContentCopyIcon />
    //                             <i className="fa-solid fa-copy"></i>
    //                         </div>
    //                     </div>
    //                 )
    //             })}
    //             <div ref={bottomRef}></div>
    //         </div>
    //     </>
    // )
}

export default MessagesSection;