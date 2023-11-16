// src/components/Home/Home.js

import React from 'react';
import {useNavigate} from 'react-router-dom';

import './Home.css';

/**
 * Home page component
 * @param {string} token - JWT token
 * @return {JSX.Element}
 */
const Home = ({token}) => {
  // useNavigate hook from react-router-dom
  const navigate = useNavigate();

  /**
   * Handle start chatting button click
   * @return {void}
   */
  const handleStartChatting = () => {
    if (token) { // if token is present, user is logged in
      navigate('/chat');
    } else { // if token is not present, user is not logged in
      navigate('/register');
    }
  };

  return (
    <div className='home-container'>
      <header>
        <h1>Welcome to imposter.ai 🤖</h1>
        <p>Start conversations with unique and interesting AI personalities.</p>
        <button onClick={handleStartChatting}>Start Chatting</button>
      </header>

      <section>
        <h2>How It Works</h2>
        <p>Imposter.AI uses the power of ChatGPT combined with our innovative
          system prompts to make our AI behave in specific ways...</p>
      </section>

      <br />

      <section>
        <h2>Our Personalities</h2>
        <p>
          David Attenborough, Anthony Bourdain, Bill Gates, Kobe Bryant,
           Lil Wayne, Henry McCord, MCU Thor, Severus Snape, Gollum,
           Tyrion Lannister
        </p>
        <p>More coming soon...</p>
      </section>

      <br />

      <section>
        <h2>Updates</h2>
        <p>Our initial personalities are up and running!
          <br />
          <br />
          We are working on adding a create custom personality feature.
        </p>
      </section>

      <br />

      <section>
        <h2>About Us</h2>
        <p>We&apos;re two friends, Tim and Christian,
          passionate about AI and its potential...
        <br />
        <br />
        If you have any suggestions, questions,
        or want to reach out in general please email us at &nbsp;
        <a
          href="mailto:imposter.ai.2023@gmail.com"
          target='_blank'
          rel='noopener noreferrer'>
            imposter.ai.2023@gmail.com
        </a>
        </p>
      </section>

      <br />

    </div>
  );
};

Home.propTypes = {
  token: PropTypes.string,
};

export default Home;
