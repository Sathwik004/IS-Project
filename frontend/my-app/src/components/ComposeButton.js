// src/components/ComposeButton.js
import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/inbox.css";

const ComposeButton = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/compose");
  };

  return (
    <button className="compose-btn" onClick={handleClick}>
      Compose
    </button>
  );
};

export default ComposeButton;
