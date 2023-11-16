// src/components/Footer/Footer.js

import React from 'react';
import {FaLinkedin, FaGithub} from 'react-icons/fa';

import './Footer.css';

const Footer = () => {
  return (
    <footer className='Footer'>
      Imposter.AI © 2023 |
      <a
        href="mailto:imposter.ai.2023@gmail.com"
        target='_blank' rel='noopener noreferrer'>Contact Us</a> |
      Follow Tim
      <a
        href="https://www.linkedin.com/in/duggant/"
        target="_blank"
        rel="noopener noreferrer"
        className="social-icon">
        <FaLinkedin />
      </a>
      <a
        href="https://github.com/trd44"
        target="_blank"
        rel="noopener noreferrer"
        className="social-icon">
        <FaGithub />
      </a>
      | Follow Christian
      <a
        href="https://www.linkedin.com/in/christianwelling/"
        target="_blank"
        rel="noopener noreferrer"
        className="social-icon">
        <FaLinkedin />
      </a>
      <a
        href="https://github.com/ChristianSAW"
        target="_blank"
        rel="noopener noreferrer"
        className="social-icon">
        <FaGithub />
      </a>
    </footer>
  );
};

export default Footer;
