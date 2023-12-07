// Navbar.tsx
import React from "react";
import { Link } from "react-router-dom";
import classes from "./navbar.module.css";

const Navbar: React.FC = () => {
  return (
    <header className={classes.header}>
      <nav>
        <ul className={classes.list}>
          <li>
            <Link to="/" className={classes.link}>
              Home
            </Link>
          </li>
          {/* <li>
            <Link to="/login" className={classes.link}>
              Login
            </Link>
          </li> */}
          <li>
            <Link to="/chat" className={classes.link}>
              Chatbot
            </Link>
          </li>
          {/* <li>
            <Link to="/spotify" className={classes.link}>
              Spotify
            </Link>
          </li> */}
          {/* <li>
            <Link to="/movies" className={classes.link}>
              Movies
            </Link>
          </li> */}
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;
