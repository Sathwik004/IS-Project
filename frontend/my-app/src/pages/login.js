// src/components/AuthForm.js
import React, { useContext, useState } from "react";
import "../styles/login.css"; // Assuming CSS is in src/styles/login.css
import { IonIcon } from "@ionic/react";
import { person, lockClosed, mail, closeCircle } from "ionicons/icons";
import { UserContext } from "../UserContext";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { algo, server } from "../constants/constants";

const Login = () => {
  const { userId, setUserId, setPrivateKey, setUniLower, setUniUpper } =
    useContext(UserContext);
  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(true);
  const [loginData, setLoginData] = useState({ username: "", password: "" });
  const [registerData, setRegisterData] = useState({
    username: "",
    email: "",
    password: "",
    public_key: "",
  });

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    console.log(loginData);

    axios
      .post(`${server}/login`, loginData)
      .then((res) => {
        console.log(res.data);
        console.log("Successfully logged in!");
        setUserId(res.data.userId);
        alert("Successfully logged in!");
        navigate("/home");
      })
      .catch((error) => {
        alert("Invalid username or password!");
        console.error("There was an error!", error);
      });
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();

    console.log(registerData);

    const generateKeysAndRegister = async () => {
      try {
        const res = await axios.get(`${algo}/generate_keys`);
        console.log(res.data.keys);
        const pk = res.data.keys["public_key"];

        if (!pk) {
          alert("Error generating public key!");
          return;
        }

        setPrivateKey(res.data.keys["private_key"]);
        setUniLower(res.data.keys["uni_inv2"]);
        setUniUpper(res.data.keys["uni_inv1"]);

        setRegisterData((prevData) => {
          const updatedData = { ...prevData, public_key: pk };
          console.log("afterr ", updatedData);

          axios
            .post(`${server}/register`, updatedData)
            .then((res) => {
              console.log(res.data);
              console.log("Successfully registered!");
              setUserId(res.data.userId);
              alert("Successfully registered in!");
              navigate("/home");
            })
            .catch((error) => {
              console.log("There was an error!", error);
            });

          return updatedData;
        });
      } catch (error) {
        console.error("An error occurred:", error);
      }
    };

    generateKeysAndRegister();
  };

  const toggleForm = () => setIsLogin(!isLogin);

  return (
    <div className={`wrapper ${!isLogin ? "active" : ""}`}>
      <a className="close-link" href="/">
        <span className="icon-close">
          <IonIcon icon={closeCircle} />
        </span>
      </a>

      {isLogin ? (
        <div className="form-box login">
          <h2>Log In</h2>
          <form onSubmit={handleLoginSubmit}>
            <div className="input-box">
              <span className="icon">
                <IonIcon icon={person} />
              </span>
              <input
                type="text"
                placeholder="Username"
                value={loginData.username}
                onChange={(e) =>
                  setLoginData({ ...loginData, username: e.target.value })
                }
                required
              />
            </div>
            <div className="input-box">
              <span className="icon">
                <IonIcon icon={lockClosed} />
              </span>
              <input
                type="password"
                placeholder="Password"
                value={loginData.password}
                onChange={(e) =>
                  setLoginData({ ...loginData, password: e.target.value })
                }
                required
              />
            </div>
            <button type="submit" className="btn">
              Log In
            </button>
            <div className="login-register">
              <p>
                New User?{" "}
                <span className="register-link" onClick={toggleForm}>
                  Register
                </span>
              </p>
            </div>
          </form>
        </div>
      ) : (
        <div className="form-box register">
          <h2>Registration</h2>
          <form onSubmit={handleRegisterSubmit}>
            <div className="input-box">
              <span className="icon">
                <IonIcon icon={person} />
              </span>
              <input
                type="text"
                placeholder="Username"
                value={registerData.username}
                onChange={(e) =>
                  setRegisterData({ ...registerData, username: e.target.value })
                }
                required
              />
            </div>
            <div className="input-box">
              <span className="icon">
                <IonIcon icon={mail} />
              </span>
              <input
                type="email"
                placeholder="Email"
                value={registerData.email}
                onChange={(e) =>
                  setRegisterData({ ...registerData, email: e.target.value })
                }
                required
              />
            </div>
            <div className="input-box">
              <span className="icon">
                <IonIcon icon={lockClosed} />
              </span>
              <input
                type="password"
                placeholder="Password"
                value={registerData.password}
                onChange={(e) =>
                  setRegisterData({
                    ...registerData,
                    password: e.target.value,
                  })
                }
                required
              />
            </div>
            <button type="submit" className="btn">
              Register
            </button>
            <div className="login-register">
              <p>
                Already have an account?{" "}
                <span className="login-link" onClick={toggleForm}>
                  Login
                </span>
              </p>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default Login;
