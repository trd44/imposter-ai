// components/FormSection.jsx

import { useState } from "react";
import SendIcon from '@mui/icons-material/Send';

const FormSection = ({generateResponse}) => {
    const [newQuestion, setNewQuestion] = useState('');

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

      const handleSubmit = () => {
        console.log('Submitting:', newQuestion);
        generateResponse(newQuestion, setNewQuestion)
      };

    return (
        <div className="form-section">
            <div style={{ flexGrow: 1}}>
            <textarea
                rows={getNumberOfLines(newQuestion) || 1}
                className="form-control"
                placeholder="Ask me anything..."
                value={newQuestion}
                onChange={(e) => setNewQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
            ></textarea>
            </div>
            <div
                className="send-icon"
                onClick={() => generateResponse(newQuestion, setNewQuestion)}
            >
                <SendIcon />
            </div>
        </div>
    )
}

export default FormSection;