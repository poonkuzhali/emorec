// src/Routes.tsx
// Routes.tsx
import React from "react";
import { Route } from "react-router-dom";
import Home from "./components/home/home";
import Chatbot from "./components/chat/chat";

const AppRoutes: React.FC = () => {
  return (
    <>
      <Route path="/" element={<Home />} />
      <Route path="/chat" element={<Chatbot />} />
    </>
  );
};

export default AppRoutes;
