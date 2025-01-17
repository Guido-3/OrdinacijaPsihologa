import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/ZakaziTermin.css";

const ZakaziTermin = () => {
  const navigate = useNavigate();
  const userId = localStorage.getItem("user_id");

  const [formData, setFormData] = useState({
    status: "zakazan",
    datum_vrijeme: "",
    nacin_izvodjenja: "uzivo",
    tip_termina_id: 1,
    klijent_id: userId,
    psiholog_id: 1,
  });

  const [error, setError] = useState(null);

  // ✅ Funkcija za validaciju datuma i vremena
  const isValidTime = (dateTime) => {
    const date = new Date(dateTime);
    const hours = date.getHours();
    const minutes = date.getMinutes();

    return hours >= 8 && hours < 16 && minutes === 0; // 📌 Vreme mora biti između 8-16h i na pun sat
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!isValidTime(formData.datum_vrijeme)) {
      setError("Vreme mora biti između 8:00 i 16:00 i na puni sat.");
      return;
    }

    try {
      const token = localStorage.getItem("token");

      await axios.post("http://localhost:8000/termin", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      alert("Termin uspešno zakazan!");
      navigate("/dashboard");
    } catch (error) {
      console.error("Greška pri zakazivanju termina:", error);
      setError(error.response?.data?.detail || "Došlo je do greške pri zakazivanju.");
    }
  };

  return (
    <div className="zakazi-termin-container">
      <h2>Zakazivanje termina</h2>
      {error && <p className="error-message">{error}</p>}

      <form onSubmit={handleSubmit}>
        {/* Datum i vreme */}
        <label>Datum i vreme:</label>
        <input
          type="datetime-local"
          name="datum_vrijeme"
          value={formData.datum_vrijeme}
          onChange={handleChange}
          required
        />

        {/* Način izvođenja */}
        <label>Način izvođenja:</label>
        <select name="nacin_izvodjenja" value={formData.nacin_izvodjenja} onChange={handleChange}>
          <option value="uzivo">Uživo</option>
          <option value="online">Online</option>
        </select>

        {/* Dugme za slanje forme */}
        <button type="submit" className="btn btn-primary">Zakaži termin</button>
      </form>
    </div>
  );
};

export default ZakaziTermin;
