import React, { Component, ChangeEvent, FormEvent } from "react";
import axios from "axios";
import "./chat.css";

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
}

class Chatbot extends Component<{}, ChatbotState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      messages: [],
      userInput: "",
      botOutput: null,
    };
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

    let data: any = "thomas"; // For the API response data: testing
    console.log(data);

    try {
      const response = await api.get(`/get?userMessage=${userMessage}`);

      if (response) {
        data = response.data;
        console.log("Here is your data");
        console.log(data);

        // Update the state with the chatbot's response
        this.setState((prevState) => ({
          messages: [...prevState.messages, { text: data.data, isUser: false }],
          botOutput: data.data,
        }));
        if (userMessage.toLowerCase() === "bye") {
          this.setState({ botOutput: data.data });
        }
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

  render() {
    return (
      <div>
        <div className="chatbox">
          {this.state.messages.map((message, index) => (
            <div
              key={index}
              className={message.isUser ? "user-message" : "chatbot-message"}
            >
              {message.isUser ? "User: " : "Chatbot: "}
              {message.text}
            </div>
          ))}
        </div>
        <form onSubmit={this.handleSubmit}>
          <input
            type="text"
            value={this.state.userInput}
            onChange={this.handleChange}
          />
          <button type="submit">Send</button>
        </form>
        {this.state.userInput.toLowerCase() === "bye" &&
          this.state.botOutput && (
            <div className="output-box">
              <p>Bot's Output:</p>
              <p>{this.state.botOutput}</p>
            </div>
          )}
      </div>
    );
  }
}

export default Chatbot;
