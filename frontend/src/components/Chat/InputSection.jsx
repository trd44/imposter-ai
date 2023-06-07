// components/InputSection.jsx

import { useState, useRef, useEffect } from "react";
import SendIcon from '@mui/icons-material/Send';

function InputSection({ onSubmit }) {
  const [message, setMessage] = useState('');
  // const textAreaRef = useRef(null); // Create a ref for the textarea
  // const maxHeight = 120

  // useEffect(() => {
  //   // Resizes textarea on component mount if there's initial content
  //   resizeTextArea();
  // }, []);

  // const resizeTextArea = () => {
  //   textAreaRef.current.style.height = 'inherit'; // Reset the height 

  //   if (textAreaRef.current.scrollHeight < maxHeight) {
  //     textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`;
  //   } else {
  //     textAreaRef.current.style.height = `${maxHeight}px`;
  //   }
  // };

  // const handleInput = (e) => {
  //   setMessage(e.target.value);
  //   resizeTextArea();
  // };
  const getNumberOfLines = (text) => {
    const maxLines = 6;
    const lines = text.split('\n').length;
    return Math.min(lines, maxLines);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // Prevent adding a new line
      handleSubmit();
    }
  };
  // const handleKeyDown = (e) => {
  //   // Enter is pressed
  //   if (e.key === 'Enter') {
  //     e.preventDefault(); // Prevent adding a new line

  //     // Shift + Enter for new line
  //     if (e.shiftKey) {
  //       setMessage((prevMessage) => prevMessage + "\n");
  //     } else {
  //       // Only Enter for submitting the form
  //       handleSubmit(e);
  //     }
  //   }
  // };

  const handleSubmit = e => {
    e.preventDefault();
    onSubmit(message);
    setMessage('');
  };

  return (
    <form className="input-form-section" onSubmit={handleSubmit}>
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
        />
      </div>
      <div
                className="send-icon"
                // onClick={() => generateResponse(newQuestion, setNewQuestion)}
            >
                <SendIcon />
            </div>
      {/* <button type="submit" className="form-button">
          <SendIcon />
        </button> */}

    </form>
  );
}

// const FormSection = ({generateResponse}) => {
//     const [newQuestion, setNewQuestion] = useState('');

//     const getNumberOfLines = (text) => {
//         const maxLines = 6;
//         const lines = text.split('\n').length;
//         return Math.min(lines, maxLines);
//       };

//       const handleKeyDown = (event) => {
//         if (event.key === 'Enter' && !event.shiftKey) {
//           event.preventDefault(); // Prevent adding a new line
//           handleSubmit();
//         }
//       };

//       const handleSubmit = () => {
//         console.log('Submitting:', newQuestion);
//         generateResponse(newQuestion, setNewQuestion)
//       };

//     return (
//         <div className="form-section">
//             <div style={{ flexGrow: 1}}>
//             <textarea
//                 rows={getNumberOfLines(newQuestion) || 1}
//                 className="form-control"
//                 placeholder="Ask me anything..."
//                 value={newQuestion}
//                 onChange={(e) => setNewQuestion(e.target.value)}
//                 onKeyDown={handleKeyDown}
//             ></textarea>
//             </div>
//             <div
//                 className="send-icon"
//                 onClick={() => generateResponse(newQuestion, setNewQuestion)}
//             >
//                 <SendIcon />
//             </div>
//         </div>
//     )
// }

export default InputSection;