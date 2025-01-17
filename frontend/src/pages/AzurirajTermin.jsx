import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import "../styles/AzurirajTermin.css";

const AzurirajTermin = () => {
  const { terminId } = useParams(); // 📌 Dobijanje ID termina iz URL-a
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    datum_vrijeme: "",
    nacin_izvodjenja: "",
  });
  const [loading, setLoading] = useState(true);

  // ✅ Dohvati podatke o terminu prilikom otvaranja stranice
  useEffect(() => {
    const fetchTermin = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`http://localhost:8000/termin/${terminId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // 📌 Postavljamo početne vrednosti forme
        setFormData({
          datum_vrijeme: response.data.datum_vrijeme,
          nacin_izvodjenja: response.data.nacin_izvodjenja,
        });

        setLoading(false);
      } catch (error) {
        console.error("Greška pri učitavanju termina:", error);
        alert("Došlo je do greške pri učitavanju termina.");
        navigate("/dashboard"); // Ako se ne može učitati, vrati korisnika na dashboard
      }
    };

    fetchTermin();
  }, [terminId, navigate]);

  // ✅ Funkcija za upravljanje unosom u formu
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // ✅ Funkcija za slanje podataka na backend
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("token");

      await axios.patch(`http://localhost:8000/termin/${terminId}`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      alert("Termin uspešno ažuriran!");
      navigate("/dashboard"); // 📌 Preusmeravanje nazad na Dashboard
    } catch (error) {
      console.error("Greška pri ažuriranju termina:", error);
      alert(error.response?.data?.detail || "Došlo je do greške pri ažuriranju.");
    }
  };

  return (
    <div className="azuriraj-termin-container">
      <h2>Ažuriranje termina</h2>
      {loading ? (
        <p>Učitavanje...</p>
      ) : (
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

          {/* Dugme za ažuriranje */}
          <button type="submit" className="btn btn-primary">Ažuriraj termin</button>
        </form>
      )}
    </div>
  );
};

export default AzurirajTermin;
