// src/components/Home/Home.js

import React from 'react';
import { useNavigate } from 'react-router-dom';

import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className='home-container'>
      <header>
        <h1>Welcome to imposter.ai 🤖</h1>
        <p>Start conversations with AI in unique roles – from travel agents to historical figures.</p>
        <button onClick={() => navigate("/chat")}>Start Chatting</button>
      </header>

      <section>
        <h2>How It Works</h2>
        <p>Imposter.AI uses the power of ChatGPT combined with our innovative system prompts to make our AI behave in specific ways...</p>
      </section>

      {/* Add additional sections to fill this up */}

      <br /> {/* This is to make the sections look separate but there is probably a better way to do this with CSS. */}
      
      <section>
        <h2>About Us</h2>
        <p>We're two friends passionate about AI and its potential...</p>
      </section>
    </div>
  );
};

export default Home;
