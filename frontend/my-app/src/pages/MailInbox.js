// src/pages/MailInbox.js
import React, { useContext, useEffect, useState } from "react";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import EmailList from "../components/EmailList";
import ComposeButton from "../components/ComposeButton";
import "../styles/inbox.css";
import axios from "axios";
import { UserContext } from "../UserContext";
import { algo, server } from "../constants/constants";

const emailsData = [
  {
    sender: "sender",
    subject: "subject",
    body: "body preview",
  },
];

const MailInbox = () => {
  const [emails, setEmails] = useState(emailsData);
  const [searchTerm, setSearchTerm] = useState("");
  const { userId, private_key, uni_lower, uni_upper } = useContext(UserContext);

  const handleSearch = (term) => {
    setSearchTerm(term.toLowerCase());
  };

  // useEffect to fetch all emails and decrypt them
  useEffect(() => {
    console.log(private_key, uni_lower, uni_upper);
    // fetch emails
    console.log("Fetching emails...", userId);
    axios
      .get(`${server}/fetch_emails`, {
        params: {
          email: userId,
        },
      })
      .then(async (response) => {
        console.log("Emails fetched successfully:", response.data);
        const decryptedEmails = await Promise.all(
          response.data.emails.map(async (email) => {
            try {
              const decryptResponse = await axios.get(`${algo}/decrypt`, {
                params: {
                  private_key: private_key,
                  encrypted_text: email.body,
                  uni_lower: uni_lower,
                  uni_upper: uni_upper,
                },
              });
              console.log(decryptResponse.data);
              const dectext = decryptResponse.data["decrypted_text"];
              return {
                sender: email.sender,
                subject: email.subject,
                body: dectext,
              };
            } catch (error) {
              console.error("An error occurred:", error);
              return {
                sender: email.sender,
                subject: email.subject,
                body: "Error decrypting email",
              };
            }
          })
        );

        console.log("Decrypted emails:", decryptedEmails);
        setEmails(decryptedEmails);
      })
      .catch((error) => {
        // handle error
        console.error("Error fetching emails:", error);
      });
  }, []);

  const filteredEmails = emails.filter(
    (email) =>
      email.sender.toLowerCase().includes(searchTerm) ||
      email.subject.toLowerCase().includes(searchTerm) ||
      email.preview.toLowerCase().includes(searchTerm)
  );

  return (
    <div>
      <Header />
      <SearchBar onSearch={handleSearch} />
      <EmailList emails={filteredEmails} />
      <ComposeButton />
    </div>
  );
};

export default MailInbox;
