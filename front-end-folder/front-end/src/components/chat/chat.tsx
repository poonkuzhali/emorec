import React, { Component, ChangeEvent, FormEvent } from "react";
import axios from "axios";
import "./chat.css";
import Modal from "react-modal";
import { Link } from "react-router-dom";

const api = axios.create({
  baseURL: " http://127.0.0.1:5000/",
});

interface Message {
  text: string;
  isUser: boolean;
}

interface ChatbotState {
  messages: Message[];
  userInput: string;
  botOutput: string | null;
  formSubmitted: boolean;
  showModal: boolean; // Add showModal state
}

class Chatbot extends Component<{}, ChatbotState> {
  chatboxRef: React.RefObject<HTMLDivElement>; // Declare chatboxRef
  constructor(props: {}) {
    super(props);
    this.state = {
      messages: [],
      userInput: "",
      botOutput: null,
      formSubmitted: false,
      showModal: false, // Add showModal state
    };
    this.chatboxRef = React.createRef();
  }

  handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    this.setState({ userInput: event.target.value });
  };

  handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    const userMessage = this.state.userInput;

    // Update the state with the user's message
    this.setState((prevState) => ({
      messages: [...prevState.messages, { text: userMessage, isUser: true }],
      userInput: "",
    }));

    let data: any; // For the API response data: testing
    // console.log(data);

    try {
      const response = await api.get(`/get?userMessage=${userMessage}`);

      if (response) {
        data = response.data;
        // console.log("Here is your data");
        console.log(data);

        // Update the state with the chatbot's response
        if (userMessage !== "bye") {
          this.setState((prevState) => ({
            messages: [...prevState.messages, { text: data, isUser: false }],
            botOutput: data,
          }));
        } else {
          this.setState((prevState) => ({
            messages: [
              ...prevState.messages,
              { text: data.emotions, isUser: false },
            ],
            botOutput: data.emotions,
            showModal: true,
          }));

          this.setState({ formSubmitted: true }); // Set formSubmitted to true
        }

        // this.setState({ formSubmitted: true }); // Set formSubmitted to true

        console.log("API Response:", response.data);
        console.log("botOutput:", this.state.botOutput);
        // Process and display the bot's response in your React component
      } else {
        // Handle the case where the response is undefined or null
        console.error("No response received from the server.");
        // You can show an error message to the user or perform other error handling here
      }
    } catch (error: any) {
      // Handle errors
      if (error.response) {
        console.error("Server responded with an error:", error.response.data);
        // You can show an error message to the user or perform other error handling here
      } else if (error.request) {
        console.error("No response received:", error.request);
        // Handle network issues, inform the user, or retry the request
      } else {
        console.error("An error occurred:", error.message);
        // Handle other errors (e.g., unexpected exceptions)
      }
    }
  };
  handleModalClose = () => {
    this.setState({ showModal: false });
  };

  render() {
    return (
      <div>
        <div className="chatbox" ref={this.chatboxRef}>
          {this.state.messages
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
        <form onSubmit={this.handleSubmit} className="input-container">
          <input
            type="text"
            value={this.state.userInput}
            onChange={this.handleChange}
            className="input-field"
          />
          <button type="submit" className="send-button">
            Send
          </button>
        </form>
        {this.state.formSubmitted &&
          this.state.userInput.toLowerCase() === "bye" && (
            <div className="output-box">
              <p>User Emotion :</p>
              {this.state.botOutput && <p>{this.state.botOutput}</p>}
            </div>
          )}
        <Modal
          isOpen={this.state.showModal}
          onRequestClose={this.handleModalClose}
          contentLabel="Bot Output Modal"
          className="custom-modal" // Apply the custom-modal class
          overlayClassName="custom-overlay" // Apply the custom-overlay class
        >
          <div className="output-box">
            <p>Your current emotion is:</p>
            {this.state.botOutput && <p>{this.state.botOutput}</p>}

            {/* Link to the Spotify component */}
            <Link to="/spotify" className="spotify-link">
              Personalized music selection for you base on your emotions
            </Link>
            <button onClick={this.handleModalClose} className="close-button">
              Close
            </button>
          </div>
        </Modal>
      </div>
    );
  }
}

export default Chatbot;
