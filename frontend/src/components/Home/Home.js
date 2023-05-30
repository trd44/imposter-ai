// src/components/Home/Home.js

import React from 'react';
import Footer from '../Footer/Footer';
import NavBar from '../NavBar/NavBar';

import './Home.css';

import FormSection from '../Chat/InputSection';
import AnswerSection from '../Chat/MessagesSection';

const Home = () => {
    // ... your state and functions ...

    return (
        <div className='home-container'>
            <NavBar />
            <header>
                <h1>Welcome to imposter.ai 🤖</h1>
                <p>Start conversations with AI in unique roles – from travel agents to historical figures.</p>
                <button>Start Chatting</button>
            </header>

            {/* <div className='content'> */}
            <section>
                <h2>How It Works</h2>
                <p>Imposter.AI uses the power of ChatGPT combined with our innovative system prompts to make our AI behave in specific ways...</p>
            </section>

            {/* <section>
        <h2>Visuals/Demo</h2>
      </section> */}

            {/* <section>
        <h2>Testimonials</h2>
      </section> */}
            <br />
            <section>
                <h2>About Us</h2>
                <p>We're two friends passionate about AI and its potential...</p>
            </section>

            {/* </div> */}

            <Footer />


            {/* </header>
      <div className="header-section">
        <h1>Imposter.AI 🤖</h1>
        <p>
        This project is a work in progress that aims to use different System prompts 
        to teach ChatGPT how to behave in various roles, such as a travel agent.
        <br/>
        <br/>
        Click send or press enter to submit your message. We are working to add an indicator that Imposter is working on an answer.
        <br/>
        <br/>
        Start by saying Hello!
        </p>
      </div> */}


            {/* <div className='app-container'>
      <div className="header-section">
        <h1>Imposter.AI 🤖</h1> */}
            {/* ... */}
            {/* </div> */}
            {/* <div className="content-wrapper">
        <div className="content-section">
          <AnswerSection storedValues={storedValues} />
        </div>
        <FormSection generateResponse={generateResponse} />
      </div> */}
            {/* </div> */}
        </div>
    );
};

export default Home;
