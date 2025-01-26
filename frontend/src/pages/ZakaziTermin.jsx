import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import "../styles/ZakaziTermin.css";

const ZakaziTermin = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const initialGroupId = searchParams.get("grupa_id"); // Ako dolazimo sa grupe, ovo se popunjava

  const userId = localStorage.getItem("user_id"); // Trenutno prijavljeni korisnik

  const [formData, setFormData] = useState({
    status: "zakazan",
    datum_vrijeme: "",
    nacin_izvodjenja: "uzivo",
    tip_termina_id: initialGroupId ? 5 : 1, // 📌 Ako je grupa -> tip_termina_id = 5 (Grupni), inače 1 (Individualni)
    klijent_id: initialGroupId ? null : userId, // 📌 Ako je individualni termin, šalje se klijent_id
    grupa_id: initialGroupId || null, // 📌 Ako je grupni termin, šalje se grupa_id
    psiholog_id: 1,
  });

  const [grupe, setGrupe] = useState([]);
  const [error, setError] = useState(null);

  // 📌 Dohvati grupe u kojima je korisnik član
  useEffect(() => {
    const fetchGrupe = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`http://localhost:8000/grupa?klijent_id=${userId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        setGrupe(response.data);
      } catch (err) {
        console.error("Greška pri učitavanju grupa:", err);
      }
    };

    fetchGrupe();
  }, [userId]);

  // 📌 Postavljanje vrednosti u formi
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 📌 Obrada promjene u dropdown-u
  const handleTerminZaChange = (e) => {
    const value = e.target.value;
    setFormData({
      ...formData,
      klijent_id: value === "individualni" ? userId : null,
      grupa_id: value !== "individualni" ? value : null,
      tip_termina_id: value === "individualni" ? 1 : 5, // Individualni = 1, Grupni = 5
    });
  };

  // 📌 Slanje podataka na backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const token = localStorage.getItem("token");
      await axios.post("http://localhost:8000/termin", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      alert("Termin uspešno zakazan!");
      if (formData.grupa_id) {
        navigate("/dashboard/grupe");
      } else {
        navigate("/dashboard");
      }
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
        <label>Termin za:</label>
        <select name="termin_za" value={formData.grupa_id ? formData.grupa_id : "individualni"} onChange={handleTerminZaChange}>
          <option value="individualni">Individualni</option>
          {grupe.map((grupa) => (
            <option key={grupa.id} value={grupa.id}>
              {grupa.naziv}
            </option>
          ))}
        </select>

        <label>Datum i vreme:</label>
        <input type="datetime-local" name="datum_vrijeme" value={formData.datum_vrijeme} onChange={handleChange} required />

        <label>Način izvođenja:</label>
        <select name="nacin_izvodjenja" value={formData.nacin_izvodjenja} onChange={handleChange}>
          <option value="uzivo">Uživo</option>
          <option value="online">Online</option>
        </select>

        <button type="submit" className="btn btn-primary">Zakaži termin</button>
      </form>
    </div>
  );
};

export default ZakaziTermin;
