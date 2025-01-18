import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState, useEffect } from "react";
import Navbar from "./components/Navbar"; 
import Home from "./pages/Home"; 
import Login from "./pages/Login"; 
import SignUp from "./pages/SignUp"; 
import Dashboard from "./pages/Dashboard";
import AzurirajTermin from "./pages/AzurirajTermin";
import ZakaziTermin from "./pages/ZakaziTermin";
import "./App.css";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem("token"));
  const [username, setUsername] = useState(localStorage.getItem("username") || "");

  // Osluškujemo promene u autentifikaciji
  useEffect(() => {
    const checkAuth = () => {
      setIsAuthenticated(!!localStorage.getItem("token"));
      setUsername(localStorage.getItem("username") || "");
    };

    window.addEventListener("authChange", checkAuth);
    return () => window.removeEventListener("authChange", checkAuth);
  }, []);

  return (
    <Router>
      <Navbar isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} username={username} /> {/* ✅ Prosleđujemo state i username */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} /> {/* ✅ Prosleđujemo funkciju za ažuriranje */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/dashboard/azuriraj/:terminId" element={<AzurirajTermin />} />
        <Route path="/dashboard/zakazi" element={<ZakaziTermin />} />
      </Routes>
    </Router>
  );
}

export default App;
