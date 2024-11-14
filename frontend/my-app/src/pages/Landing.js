import React from "react";
import Header from "../components/Header";
import "../styles/styles.css";
import securityImage from "../assets/undraw_security_re_a2rk.svg";
import randomlines from "../assets/random lines.svg";

function Landing() {
  return (
    <div>
      <Header />
      <div className="oval1">
        <img src="./Images/Oval (1).svg" alt="ovalimage" />
      </div>
      <div className="oval2">
        <img src="./Images/Oval (1).svg" alt="ovalimage" />
      </div>
      <div className="card">
        <h2>Shield Share</h2>
        <p>
          In a world where data privacy is more important than ever, Shield
          Share provides a fast, user-friendly, and highly secure way to share
          your data. Whether you're sending personal data or critical business
          data, our platform ensures your files remain protected every step of
          the way.
        </p>
      </div>
      <div className="imagemain">
        <img src={securityImage} width="450" alt="imagemain" />
      </div>
      <div class="randomimg">
        <img src={randomlines} alt="" />
      </div>
    </div>
  );
}

export default Landing;
