import React, { Component, ChangeEvent, FormEvent } from "react";

interface Message {
  text: string;
  isUser: boolean;
}

interface ChatbotState {
  messages: Message[];
  userInput: string;
}

class Chatbot extends Component<{}, ChatbotState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      messages: [],
      userInput: "",
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

    // Send the user's message to the server
    const response = await fetch(`/api/chat?message=${userMessage}`);
    const data = await response.json();

    // Update the state with the chatbot's response
    this.setState((prevState) => ({
      messages: [...prevState.messages, { text: data.message, isUser: false }],
    }));
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
      </div>
    );
  }
}

export default Chatbot;
