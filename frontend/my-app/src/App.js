import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/home";
import Login from "./pages/login";
import NoPage from "./pages/nopage";
import { UserProvider, UserContext } from "./UserContext";
import { useContext } from "react";
import Landing from "./pages/Landing";
import ComposeEmail from "./pages/ComposeEmail";

function Content() {
  const { userId, privateKey, uniLower, uniUpper } = useContext(UserContext);
  console.log(userId, privateKey, uniLower, uniUpper);
  return (
    <Router>
      {userId ? (
        <Routes>
          <Route index element={<Landing />} />
          <Route path="/home" element={<Home />} />
          <Route path="/compose" element={<ComposeEmail />} />
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<NoPage />} />
        </Routes>
      ) : (
        <Routes>
          <Route index element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<NoPage />} />
        </Routes>
      )}
    </Router>
  );
}

function App() {
  return (
    <UserProvider>
      <Content />
    </UserProvider>
  );
}

export default App;
