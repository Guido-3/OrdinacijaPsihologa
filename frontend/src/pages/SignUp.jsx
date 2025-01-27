import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { jwtDecode } from "jwt-decode"; // ✅ Dekodiranje tokena
import "../styles/SignUp.css"; // CSS za stilizaciju

const SignUp = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    ime: "",
    prezime: "",
    username: "",
    email: "",
    datum_rodjenja: "",
    broj_telefona: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Resetujemo greške

    if (formData.password !== formData.confirmPassword) {
      setError("Lozinke se ne poklapaju.");
      return;
    }

    try {
      // 1️⃣ Kreiramo klijenta
      const response = await axios.post(
        "http://localhost:8000/klijent",
        {
          ime: formData.ime,
          prezime: formData.prezime,
          username: formData.username,
          email: formData.email,
          datum_rodjenja: formData.datum_rodjenja,
          broj_telefona: formData.broj_telefona,
          hashed_password: formData.password,
        },
        { headers: { "Content-Type": "application/json" } }
      );

      console.log("✅ Registracija uspešna:", response.data);

      // 2️⃣ Automatski prijavljujemo korisnika nakon registracije
      const loginResponse = await axios.post(
        "http://localhost:8000/auth/login",
        new URLSearchParams({
          username: formData.username,
          password: formData.password,
        }),
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
      );

      const token = loginResponse.data.access_token;
      localStorage.setItem("token", token);

      // 3️⃣ Dekodiranje tokena za user_id i username (ISTO KAO U LOGINU)
      const decoded = jwtDecode(token);
      console.log("✅ Dekodirani token:", decoded);

      const userId = decoded.id;
      const username = decoded.sub; // ✅ Dohvatanje username-a

      if (!userId || !username) {
        throw new Error("Podaci korisnika nisu pronađeni u tokenu.");
      }

      // 4️⃣ Čuvamo user_id i username u localStorage (ISTO KAO U LOGINU)
      localStorage.setItem("user_id", userId);
      localStorage.setItem("username", username);

      // 5️⃣ Ažuriramo stanje autentifikacije i navbar
      setIsAuthenticated(true);
      window.dispatchEvent(new Event("authChange")); // 🚀 Trigguje ažuriranje Navbara

      // 6️⃣ Preusmeravamo korisnika na dashboard
      navigate("/dashboard");

    } catch (error) {
      console.error("❌ Greška prilikom registracije:", error);

      // Sigurno postavljanje poruke greške
      setError(
        error.response?.data?.detail || "Došlo je do greške prilikom registracije."
      );
    }
  };

  return (
    <div className="signup-container">
      <h2>Registracija</h2>
      {error && <p className="error-message">{typeof error === "string" ? error : "Došlo je do greške"}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" name="ime" placeholder="Ime" value={formData.ime} onChange={handleChange} required />
        <input type="text" name="prezime" placeholder="Prezime" value={formData.prezime} onChange={handleChange} required />
        <input type="text" name="username" placeholder="Korisničko ime" value={formData.username} onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <input type="date" name="datum_rodjenja" value={formData.datum_rodjenja} onChange={handleChange} required />
        <input type="text" name="broj_telefona" placeholder="Broj telefona" value={formData.broj_telefona} onChange={handleChange} required />
        <input type="password" name="password" placeholder="Lozinka" value={formData.password} onChange={handleChange} required />
        <input type="password" name="confirmPassword" placeholder="Potvrdite lozinku" value={formData.confirmPassword} onChange={handleChange} required />
        <button type="submit" className="btn btn-primary">Registracija</button>
      </form>
    </div>
  );
};

export default SignUp;
