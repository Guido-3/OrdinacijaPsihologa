import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // ✅ Importujemo useNavigate za preusmeravanje
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import "../styles/NapraviGrupu.css";

const NapraviGrupu = () => {
  const navigate = useNavigate(); // ✅ Hook za preusmeravanje
  const [nazivGrupe, setNazivGrupe] = useState("");
  const [opisGrupe, setOpisGrupe] = useState("");
  const [usernames, setUsernames] = useState([""]);
  const [currentUser, setCurrentUser] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // ✅ Dohvati username iz JWT tokena pri prvom učitavanju
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        setCurrentUser(decoded.sub); // ✅ "sub" u tokenu sadrži username
      } catch (error) {
        console.error("Greška pri dekodiranju tokena:", error);
      }
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!nazivGrupe || usernames.length < 1) {
      setError("Naziv grupe i minimum jedan dodatni korisnik su obavezni.");
      return;
    }

    try {
      const token = localStorage.getItem("token");
      await axios.post(
        "http://localhost:8000/grupa",
        {
          naziv: nazivGrupe,
          opis: opisGrupe,
          klijenti_usernames: [currentUser, ...usernames], // ✅ Automatski dodajemo ulogovanog korisnika
        },
        { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } }
      );

      setSuccess("Grupa uspešno kreirana!");

      // ✅ Resetujemo formu
      setNazivGrupe("");
      setOpisGrupe("");
      setUsernames([""]);

      // ✅ Nakon 1.5 sekunde preusmeravamo na "/dashboard/grupe"
      setTimeout(() => {
        navigate("/dashboard/grupe");
      }, 1500);
    } catch (err) {
      console.error("Greška pri kreiranju grupe:", err);
      setError(err.response?.data?.detail || "Došlo je do greške pri kreiranju grupe.");
    }
  };

  const handleUsernameChange = (index, value) => {
    const updatedUsernames = [...usernames];
    updatedUsernames[index] = value;
    setUsernames(updatedUsernames);
  };

  const handleAddUsername = () => {
    setUsernames([...usernames, ""]);
  };

  return (
    <div className="napravi-grupu-container">
      <h2>Napravi novu grupu</h2>
      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}

      <form onSubmit={handleSubmit}>
        <label>Naziv grupe:</label>
        <input type="text" value={nazivGrupe} onChange={(e) => setNazivGrupe(e.target.value)} required />

        <label>Opis grupe (opciono):</label>
        <textarea value={opisGrupe} onChange={(e) => setOpisGrupe(e.target.value)} rows="3" />

        <h3>Unesite username-ove članova:</h3>
        {usernames.map((username, index) => (
          <input
            key={index}
            type="text"
            placeholder="Unesite username"
            value={username}
            onChange={(e) => handleUsernameChange(index, e.target.value)}
            required
          />
        ))}
        <button type="button" className="btn-add" onClick={handleAddUsername}>
          Dodaj još jednog člana
        </button>

        <button type="submit" className="btn btn-primary">Kreiraj grupu</button>
      </form>
    </div>
  );
};

export default NapraviGrupu;
