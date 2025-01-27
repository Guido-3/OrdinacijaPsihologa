import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "../styles/DashboardGrupe.css";

const DashboardGrupe = () => {
  const [grupe, setGrupe] = useState([]);
  const [terminiGrupe, setTerminiGrupe] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const userId = localStorage.getItem("user_id"); // Trenutno prijavljeni korisnik

  useEffect(() => {
    const fetchGrupe = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!userId) {
          setError("ID korisnika nije pronađen.");
          setLoading(false);
          return;
        }

        const response = await axios.get(`http://localhost:8000/grupa?klijent_id=${userId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        setGrupe(response.data);
        setLoading(false);
      } catch (err) {
        setError("Greška pri učitavanju grupa.");
        setLoading(false);
      }
    };

    fetchGrupe();
  }, [userId]);

  // Funkcija za dohvaćanje termina za određenu grupu
  const fetchTerminiZaGrupu = async (grupaId) => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get(`http://localhost:8000/termin/grupa/${grupaId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setTerminiGrupe((prev) => ({
        ...prev,
        [grupaId]: response.data,
      }));
    } catch (error) {
      console.error(`Greška pri učitavanju termina za grupu ${grupaId}:`, error);
      setTerminiGrupe((prev) => ({
        ...prev,
        [grupaId]: [],
      }));
    }
  };

  // Funkcija za brisanje grupe
  const handleDelete = async (grupaId) => {
    const confirmDelete = window.confirm("Da li ste sigurni da želite da obrišete ovu grupu?");
    if (!confirmDelete) return;

    try {
      const token = localStorage.getItem("token");
      await axios.delete(`http://localhost:8000/grupa/${grupaId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setGrupe((prevGrupe) => prevGrupe.filter((grupa) => grupa.id !== grupaId));
      setTerminiGrupe((prev) => {
        const updatedTermini = { ...prev };
        delete updatedTermini[grupaId];
        return updatedTermini;
      });
    } catch (error) {
      console.error("Greška pri brisanju grupe:", error);
      alert("Došlo je do greške pri brisanju grupe.");
    }
  };

  return (
    <div className="dashboard-grupe-container">
      <h1>Moje grupe</h1>

      {/* Dugme za kreiranje nove grupe */}
      <div className="kreiraj-grupu">
        <Link to="/dashboard/grupe/napravi" className="btn btn-primary">Napravi grupu</Link>
      </div>

      {loading ? (
        <p>Učitavanje...</p>
      ) : error ? (
        <p className="error-message">{error}</p>
      ) : grupe.length === 0 ? (
        <p>Nemate nijednu grupu.</p>
      ) : (
        <div className="grupe-list">
          {grupe.map((grupa) => (
            <div key={grupa.id} className="grupa-card">
              <div className="grupa-header">
                <h3>{grupa.naziv}</h3>
                <p>{grupa.opis}</p>
              </div>

              {/* Dugmad za upravljanje grupom */}
              <div className="grupa-actions">
                <Link to={`/dashboard/grupe/azuriraj/${grupa.id}`} className="btn-update">Ažuriraj</Link>
                <button className="btn-delete" onClick={() => handleDelete(grupa.id)}>Obriši</button>
                <Link to="/dashboard/zakazi" className="btn-secondary">Zakazi termin</Link>
              </div>

              {/* Accordion sekcija za termine grupe */}
              <details onClick={() => !terminiGrupe[grupa.id] && fetchTerminiZaGrupu(grupa.id)}>
                <summary>Prikaži termine</summary>
                <ul className="termini-list">
                  {terminiGrupe[grupa.id] && terminiGrupe[grupa.id].length > 0 ? (
                    terminiGrupe[grupa.id].map((termin) => (
                      <li key={termin.id} className="termin-card">
                        <p><strong>Datum i vreme:</strong> {new Date(termin.datum_vrijeme).toLocaleString()}</p>
                        <p><strong>Način izvođenja:</strong> {termin.nacin_izvodjenja}</p>
                        <div className="termin-actions">
                          <Link to={`/dashboard/azuriraj/${termin.id}`} className="btn-update">Ažuriraj</Link>
                          <button className="btn-delete" onClick={() => handleDelete(termin.id)}>Izbriši</button>
                        </div>
                      </li>
                    ))
                  ) : (
                    <p>Ova grupa nema zakazane termine.</p>
                  )}
                </ul>
              </details>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DashboardGrupe;