import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { jwtDecode } from "jwt-decode"; // ✅ Ispravan import
import "../styles/Login.css"; 
const Login = ({ setIsAuthenticated }) => {  // ✅ Primamo funkciju iz App.jsx
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const formDataParams = new URLSearchParams();
      formDataParams.append("username", formData.username);
      formDataParams.append("password", formData.password);

      const response = await axios.post("http://localhost:8000/auth/login", formDataParams, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      console.log("Prijava uspešna:", response.data);

      const token = response.data.access_token;
      localStorage.setItem("token", token);

      const decoded = jwtDecode(token);
      console.log("Dekodirani token:", decoded);

      const userId = decoded.id;
      if (!userId) {
        throw new Error("ID korisnika nije pronađen u tokenu.");
      }

      localStorage.setItem("user_id", userId);

      setIsAuthenticated(true); // ✅ Odmah osvežavamo stanje
      window.dispatchEvent(new Event("authChange")); // ✅ Obaveštavamo aplikaciju o promeni
      navigate("/dashboard");
    } catch (error) {
      console.error("Greška prilikom prijave:", error.response?.data || error.message);
      setError(error.response?.data?.detail || "Neispravno korisničko ime ili lozinka.");
    }
  };

  return (
    <div className="login-container">
      <h2>Prijava</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" name="username" placeholder="Korisničko ime" value={formData.username} onChange={handleChange} required />
        <input type="password" name="password" placeholder="Lozinka" value={formData.password} onChange={handleChange} required />
        <button type="submit" className="btn btn-primary">Prijava</button>
      </form>
    </div>
  );
};

export default Login;
