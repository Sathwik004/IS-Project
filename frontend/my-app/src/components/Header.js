import React, { useContext } from "react";
import "../styles/styles.css";
import { UserContext } from "../UserContext";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();
  function onLogout() {
    localStorage.removeItem("userId");
    navigate("/landing");
  }
  const { userId } = useContext(UserContext);
  return (
    <header className="header">
      <a href="#" className="logo">
        Shield Share
      </a>
      <nav className="navbar">
        <a className="navlink" href="./home">
          Home
        </a>
        <a className="navlink" href="./about">
          About
        </a>
        <a href="./login">
          <button className="login" onClick={onLogout}>
            {userId ? "Log Out" : "Log In"}
          </button>
        </a>
      </nav>
    </header>
  );
};

export default Header;
