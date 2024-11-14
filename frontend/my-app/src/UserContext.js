import React, { createContext, useState, useEffect } from "react";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [userId, setUserId] = useState(() => {
    return localStorage.getItem("userId") || null;
  });
  const [private_key, setPrivateKey] = useState(() => {
    const userData = JSON.parse(localStorage.getItem("userData")) || {};
    return userData[userId]?.private_key || null;
  });
  const [uni_upper, setUniUpper] = useState(() => {
    const userData = JSON.parse(localStorage.getItem("userData")) || {};
    return userData[userId]?.uni_upper || null;
  });
  const [uni_lower, setUniLower] = useState(() => {
    const userData = JSON.parse(localStorage.getItem("userData")) || {};
    return userData[userId]?.uni_lower || null;
  });

  useEffect(() => {
    if (userId) {
      localStorage.setItem("userId", userId);
    } else {
      localStorage.removeItem("userId");
    }
  }, [userId]);

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem("userData")) || {};
    if (private_key) {
      userData[userId] = { ...userData[userId], private_key };
      localStorage.setItem("userData", JSON.stringify(userData));
    } else if (userData[userId]) {
      delete userData[userId].private_key;
      localStorage.setItem("userData", JSON.stringify(userData));
    }
  }, [private_key, userId]);

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem("userData")) || {};
    if (uni_upper) {
      userData[userId] = { ...userData[userId], uni_upper };
      localStorage.setItem("userData", JSON.stringify(userData));
    } else if (userData[userId]) {
      delete userData[userId].uni_upper;
      localStorage.setItem("userData", JSON.stringify(userData));
    }
  }, [uni_upper, userId]);

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem("userData")) || {};
    if (uni_lower) {
      userData[userId] = { ...userData[userId], uni_lower };
      localStorage.setItem("userData", JSON.stringify(userData));
    } else if (userData[userId]) {
      delete userData[userId].uni_lower;
      localStorage.setItem("userData", JSON.stringify(userData));
    }
  }, [uni_lower, userId]);

  return (
    <UserContext.Provider
      value={{
        userId,
        setUserId,
        private_key,
        uni_upper,
        uni_lower,
        setPrivateKey,
        setUniLower,
        setUniUpper,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
