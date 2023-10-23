import React from "react";
import { Link } from "react-router-dom";
import classes from "./navbar.module.css";

const Navbar: React.FC = () => {
  return (
    <header className={classes.header}>
      <nav>
        <ul className={classes.list}>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/login">Login</Link>
          </li>
          <li>
            <Link to="chat">Chatbot</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;
