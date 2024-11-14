// src/components/ComposeEmail.js
import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/compose.css";
import Header from "../components/Header";
import axios from "axios";
import { algo, server } from "../constants/constants";
import { UserContext } from "../UserContext";

const ComposeEmail = () => {
  const { userId } = useContext(UserContext);
  const [recipient, setRecipient] = useState("");
  const [subject, setSubject] = useState("");
  const [emailBody, setEmailBody] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    axios
      .get(`${server}/get_public_key`, {
        params: {
          email: recipient,
        },
      })
      .then((response) => {
        if (response.status === 200) {
          const publicKey = response.data.public_key;
          console.log("Public Key:", publicKey);
          // You can now use the public key as needed

          axios
            .post(`${algo}/encrypt`, {
              public_key: publicKey,
              message: emailBody,
            })
            .then((response) => {
              console.log("Response:", response.data);
              console.log(
                "Encrypted Message:",
                response.data["encrypted_text"]
              );

              // axios req to send and store enc email
              axios
                .post(`${server}/send_email`, {
                  sender: userId,
                  reveiver: recipient,
                  subject: subject,
                  body: response.data["encrypted_text"],
                })
                .then((response) => {
                  console.log("Response:", response.data);
                  navigate("/home");
                })
                .catch((error) => {
                  console.error("An error occurred:", error);
                });
            })
            .catch((error) => {
              console.log("An error occurred:", error);
            });
        } else {
          console.log("Error:", response.data.message);
        }
      })
      .catch((error) => {
        console.error("An error occurred:", error);
      });

    // alert("Email sent!");
    // navigate("/inbox"); // Navigate back to inbox
  };

  return (
    <div>
      <Header />

      <div className="compose-container">
        <h2>Compose New Email</h2>
        <form onSubmit={handleSubmit} id="composeForm">
          <input
            id="recipient"
            type="text"
            placeholder="To:"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            required
          />
          <input
            id="subject"
            type="text"
            placeholder="Subject:"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            required
          />
          <textarea
            placeholder="Write your email here..."
            value={emailBody}
            onChange={(e) => setEmailBody(e.target.value)}
            required
          />
          <button type="submit" className="send-btn">
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ComposeEmail;
