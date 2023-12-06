// Inside your Home component

import React, { Component } from "react";
import { Link } from "react-router-dom";
import "./home.css"; // Import your CSS file

class Home extends Component {
  render() {
    return (
      <div className="home-container">
        <div className="content-container">
          <h1 className="highlighted-text">Emorec</h1>
          <p className="description">Emotion-based content recommendation</p>
          <div className="cta-container">
            <Link to="/chat" className="cta-button">
              Start Chatting
            </Link>
          </div>
        </div>
        <div className="learn-more-container">
          <Link to="/about" className="cta-link">
            Learn More
          </Link>
        </div>
      </div>
    );
  }
}

export default Home;
