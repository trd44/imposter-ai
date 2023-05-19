// components/AnswerSection.jsx
import React, { useEffect, useRef } from 'react';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';


const AnswerSection = ({ storedValues }) => {
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
        <>
            <hr className="hr-line" />
            <div className="answer-container">
                {[...storedValues].reverse().map((value, index) => {
                    return (
                        <div className="answer-section" key={index}>
                            <p className="question">{value.question}</p>
                            <p className="answer">{value.answer}</p>
                            <div
                                className="copy-icon"
                                onClick={() => copyText(value.answer)}
                            >
                                <ContentCopyIcon />
                                <i className="fa-solid fa-copy"></i>
                            </div>
                        </div>
                    )
                })}
                <div ref={bottomRef}></div>
            </div>
        </>
    )
}

export default AnswerSection;