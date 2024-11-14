// src/components/SearchBar.js
import React from "react";
import "../styles/inbox.css";

const SearchBar = ({ onSearch }) => (
  <div className="search-container">
    <input
      id="searchInput"
      type="text"
      placeholder="Search emails..."
      onChange={(e) => onSearch(e.target.value)}
    />
  </div>
);

export default SearchBar;
