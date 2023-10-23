// src/components/Home.tsx
import React, { Component } from "react";
import { Link } from "react-router-dom";

class Home extends Component {
  render() {
    return (
      <div>
        <h1>Welcome to the Home Page</h1>
        <p>
          {" "}
          <Link to="/chat">Go to Chat Box</Link>
        </p>
      </div>
    );
  }
}

export default Home;
