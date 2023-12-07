import React, { useState, useRef, ChangeEvent, FormEvent } from "react";
import axios from "axios";
import "./chat.css";
import Modal from "react-modal";
import { Link, useNavigate } from "react-router-dom";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/",
});

interface Message {
  text: string;
  isUser: boolean;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState<string>("");
  const [botOutput, setBotOutput] = useState<string | null>(null);
  const [formSubmitted, setFormSubmitted] = useState<boolean>(false);
  const [showModal, setShowModal] = useState<boolean>(false);

  const chatboxRef = useRef<HTMLDivElement>(null);

  // const navigate = useNavigate();

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    const userMessage = userInput;

    // Update the state with the user's message
    setMessages((prevState) => [
      ...prevState,
      { text: userMessage, isUser: true },
    ]);
    setUserInput("");

    let data: any; // For the API response data: testing

    try {
      const response = await api.get(`/get?userMessage=${userMessage}`);

      if (response) {
        data = response.data;

        // Update the state with the chatbot's response
        if (userMessage !== "bye") {
          setMessages((prevState) => [
            ...prevState,
            { text: data, isUser: false },
          ]);
          setBotOutput(data);
        } else {
          setMessages((prevState) => [
            ...prevState,
            { text: data.emotions, isUser: false },
          ]);
          setBotOutput(data.emotions);
          setShowModal(true);
          setFormSubmitted(true);
        }
      }
    } catch (error: any) {
      // Handle errors
      console.error("An error occurred:", error.message);
    }
  };

  const handleModalClose = () => {
    setShowModal(false);
  };

  const handleImage1LinkClick = async (emotionUser: any) => {
    try {
      // Make API call to /spotify
      const response = await api.get(`/spotify/${emotionUser}`);

      window.open(response.data, "_blank");

      console.log(response.data);
    } catch (error) {
      // Handle errors
      console.error("An error occurred:", error);
    }
  };

  const handleImage2LinkClick = async (emotionUser: any) => {
    try {
      // Make API call to /spotify
      const response = await api.get("/movies");

      // navigate("/movies", { state: { movies: response.data } });

      // If you want to pass state, you can use localStorage or another mechanism to store the data
      localStorage.setItem("moviesData", JSON.stringify(response.data));
      // Open a new window with the "/movies" URL and pass the data as state
      window.open("/movies", "_blank");
    } catch (error) {
      // Handle errors
      console.error("An error occurred:", error);
    }
  };

  return (
    <div>
      <div className="chatbox" ref={chatboxRef}>
        {messages
          .filter((message) => message.text.toLowerCase() !== "bye")
          .map((message, index) => (
            <div
              key={index}
              className={message.isUser ? "user-message" : "chatbot-message"}
            >
              {message.isUser ? "You: " : "Chatbot: "}
              {message.text}
            </div>
          ))}
      </div>
      <form onSubmit={handleSubmit} className="input-container">
        <input
          type="text"
          value={userInput}
          onChange={handleChange}
          className="input-field"
        />
        <button type="submit" className="send-button">
          Send
        </button>
      </form>
      {formSubmitted && userInput.toLowerCase() === "bye" && (
        <div className="output-box">
          <p>User Emotion :</p>
          {botOutput && <p>{botOutput}</p>}
        </div>
      )}
      <Modal
        isOpen={showModal}
        onRequestClose={handleModalClose}
        contentLabel="Bot Output Modal"
        className="custom-modal" // Apply the custom-modal class
        overlayClassName="custom-overlay" // Apply the custom-overlay class
      >
        <div className="output-box">
          <p>
            Your current emotion is:
            {botOutput && <strong>{botOutput}</strong>}
          </p>

          {/* Link to the Spotify component */}
          {/* <Link to="/spotify" className="spotify-link">
              Personalized music selection for you based on your emotions
            </Link> */}

          <div className="image-links">
            <a
              onClick={() => handleImage1LinkClick(botOutput)}
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                src="data:image/png;base64,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"
                alt="Image 1"
                style={{ width: "100px", height: "100px" }}
              />
            </a>
            <a
              onClick={() => handleImage2LinkClick(botOutput)}
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                src="data:image/png;base64,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"
                alt="Image 2"
                style={{ width: "100px", height: "100px" }}
              />
            </a>
          </div>

          <button onClick={handleModalClose} className="close-button">
            Close
          </button>
        </div>
      </Modal>
    </div>
  );
};

export default Chatbot;
