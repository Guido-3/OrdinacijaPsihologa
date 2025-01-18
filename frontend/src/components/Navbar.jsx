import { Link, useNavigate } from "react-router-dom";
import "../styles/Navbar.css";

const Navbar = ({ isAuthenticated, setIsAuthenticated, username }) => { // Dodali smo username kao prop
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username"); // Brisanje korisnickog imena
    setIsAuthenticated(false);
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
              <span className="navbar-username">{username}</span> {/* Prikaz korisnickog imena */}
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