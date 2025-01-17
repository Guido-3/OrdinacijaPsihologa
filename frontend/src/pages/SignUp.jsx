import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/SignUp.css"; // CSS za stilizaciju

const SignUp = () => {
  const navigate = useNavigate(); // Omogućava preusmeravanje nakon registracije
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

  // Funkcija za upravljanje unosom u formu
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Funkcija za slanje podataka na backend
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Provera da li se lozinke poklapaju
    if (formData.password !== formData.confirmPassword) {
      setError("Lozinke se ne poklapaju.");
      return;
    }

    try {
      // Slanje podataka na backend
      const response = await axios.post("http://localhost:8000/klijent", {
        ime: formData.ime,
        prezime: formData.prezime,
        username: formData.username,
        email: formData.email,
        datum_rodjenja: formData.datum_rodjenja,
        broj_telefona: formData.broj_telefona,
        hashed_password: formData.password, // Backend očekuje hashed_password
      },
      {
        headers: { "Content-Type": "application/json" }, // **Ispravan format**
      }
    );

      console.log("Registracija uspešna:", response.data);

      // Automatska prijava korisnika nakon registracije
      const loginResponse = await axios.post(
        "http://localhost:8000/auth/login",
        new URLSearchParams({
          username: formData.username,
          password: formData.password,
        }),
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );

      // Čuvanje JWT tokena u localStorage
      localStorage.setItem("token", loginResponse.data.access_token);

      // Preusmeravanje na korisničku stranicu
      navigate("/dashboard");
    } catch (error) {
      console.error("Greška prilikom registracije:", error.response?.data || error.message);
      setError(error.response?.data?.detail || "Došlo je do greške prilikom registracije.");
    }
  };

  return (
    <div className="signup-container">
      <h2>Registracija</h2>
      {error && <p className="error-message">{error}</p>}
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
