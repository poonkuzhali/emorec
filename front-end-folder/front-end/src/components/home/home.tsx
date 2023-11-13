import React, { Component } from "react";
import { Link } from "react-router-dom";
import "./home.css"; // Import your CSS file

class Home extends Component {
  render() {
    return (
      <div className="home-container">
        <h1 className="highlighted-text">Welcome to Emorec App</h1>
        <p className="description">
          Explore the power of emotions with Emorec App. Connect with others,
          share your feelings, and experience the joy of emotional expression.
        </p>
        <div className="cta-container">
          <Link to="/chat" className="cta-button">
            Start Chatting
          </Link>
          <Link to="/about" className="cta-link">
            Learn More
          </Link>
        </div>
      </div>
    );
  }
}

export default Home;
