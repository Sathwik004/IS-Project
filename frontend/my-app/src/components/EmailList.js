// src/components/EmailList.js
import React from "react";
import "../styles/inbox.css";

const EmailList = ({ emails }) => (
  <div className="main email-list">
    {emails.map((email, index) => (
      <div key={index} className="email-item">
        <div className="sender">{email.sender}</div>
        <div className="subject">{email.subject}</div>
        <div className="preview">{email.body}</div>
      </div>
    ))}
  </div>
);

export default EmailList;
