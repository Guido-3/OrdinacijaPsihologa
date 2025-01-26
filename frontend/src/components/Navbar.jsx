import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode"; // ✅ Import za dekodiranje tokena
import "../styles/Navbar.css";

const Navbar = ({ isAuthenticated, setIsAuthenticated }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState(""); // ✅ State za username

  // ✅ Provera da li je korisnik prijavljen i dekodiranje tokena
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        setUsername(decoded.sub); // ✅ "sub" u tokenu sadrži username
      } catch (error) {
        console.error("Greška pri dekodiranju tokena:", error);
      }
    } else {
      setUsername(""); // Ako korisnik nije prijavljen, brišemo username
    }
  }, [isAuthenticated]); // ✅ Osluškujemo promene u autentifikaciji

  // ✅ Funkcija za odjavu
  const handleLogout = () => {
    localStorage.removeItem("token"); 
    setIsAuthenticated(false);
    setUsername(""); // ✅ Brišemo username
    window.dispatchEvent(new Event("authChange"));
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">Ordinacija Psihologa</Link>

        <div className="navbar-buttons">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="navbar-link">Moji termini</Link>
              <Link to="/dashboard/grupe" className="navbar-link">Moje grupe</Link>
              <Link to="/dashboard/zakazi" className="navbar-link">Zakazi termin</Link>
              <Link to="/dashboard/grupe/napravi" className="navbar-link">Napravi grupu</Link> {/* ✅ Novo dugme */}
              <span className="navbar-username">👤 {username}</span> {/* ✅ Prikaz username-a */}
              <button onClick={handleLogout} className="navbar-button logout-button">Odjavi se</button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-button">Prijava</Link>
              <Link to="/signup" className="navbar-button">Registracija</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
