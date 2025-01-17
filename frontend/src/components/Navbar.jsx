import { Link, useNavigate } from "react-router-dom";
import "../styles/Navbar.css"; 

const Navbar = ({ isAuthenticated, setIsAuthenticated }) => {  // ✅ Primamo stanje iz App.jsx
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token"); 
    setIsAuthenticated(false); // ✅ Direktno ažuriramo stanje
    window.dispatchEvent(new Event("authChange")); // ✅ Obaveštavamo aplikaciju o promeni
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
