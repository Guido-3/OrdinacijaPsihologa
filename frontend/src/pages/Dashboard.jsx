import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "../styles/Dashboard.css";

const Dashboard = () => {
  const [termini, setTermini] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTermini = async () => {
      try {
        const token = localStorage.getItem("token");
        const userId = localStorage.getItem("user_id");

        if (!userId) {
          setError("ID korisnika nije pronađen.");
          setLoading(false);
          return;
        }

        const response = await axios.get(`http://localhost:8000/termin?klijent_id=${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const futureTermini = response.data.filter(
          (termin) => new Date(termin.datum_vrijeme) >= new Date()
        );

        setTermini(futureTermini);
        setLoading(false);
      } catch (err) {
        setError("Greška pri učitavanju termina.");
        setLoading(false);
      }
    };

    fetchTermini();
  }, []);

  // Funkcija za brisanje termina
  const handleDelete = async (terminId) => {
    const confirmDelete = window.confirm("Da li ste sigurni da želite da obrišete ovaj termin?");
    
    if (!confirmDelete) return; // Ako korisnik odustane, ništa se ne dešava

    try {
      const token = localStorage.getItem("token");
      await axios.delete(`http://localhost:8000/termin/${terminId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // Ažuriranje stanja da bi se termin uklonio sa liste bez osvežavanja stranice
      setTermini((prevTermini) => prevTermini.filter((termin) => termin.id !== terminId));
    } catch (error) {
      console.error("Greška pri brisanju termina:", error);
      alert("Došlo je do greške pri brisanju termina.");
    }
  };

  return (
    <div className="dashboard-container">
      <h1>Moji budući termini</h1>

      {/* Sekcija za prikaz termina */}
      <div className="termini-list">
        {loading ? (
          <p>Učitavanje...</p>
        ) : error ? (
          <p className="error-message">{error}</p>
        ) : termini.length === 0 ? (
          <p>Nemate zakazane termine.</p>
        ) : (
          termini.map((termin) => (
            <div key={termin.id} className="termin-card">
              <p><strong>Datum i vreme:</strong> {new Date(termin.datum_vrijeme).toLocaleString()}</p>
              <p><strong>Način izvođenja:</strong> {termin.nacin_izvodjenja}</p>
              
              {/* Dugme za ažuriranje termina */}
              <div className="termin-actions">
                <Link to={`/dashboard/azuriraj/${termin.id}`} className="btn-update">
                  Ažuriraj
                </Link>
                <button className="btn-delete" onClick={() => handleDelete(termin.id)}>
                  Izbriši
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Sekcija za dugme "Zakazi novi termin" */}
      <div className="zakazi-sekcija">
        <Link to="/dashboard/zakazi" className="btn btn-primary">Zakazi novi termin</Link>
      </div>
    </div>
  );
};

export default Dashboard;
