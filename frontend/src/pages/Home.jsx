import { Link } from "react-router-dom";
import "../styles/Home.css";
import psiholoskinjaImg from "../photos/psiholoskinja.png";

const Home = () => {
  return (
    <>
      <div className="home-container">
        {/* Sekcija sa slikom psihološkinje */}
        <div className="profile-section">
          <img
            src={psiholoskinjaImg}
            alt="Ana Jovanović"
            className="profile-image"
          />
          <h2>Dr. Ana Jovanović</h2>
          <p className="profile-info">
            Specijalista za individualnu, grupnu i porodičnu terapiju. Sa preko
            10 godina iskustva, Ana je posvećena pružanju vrhunske psihološke
            podrške.
          </p>
        </div>

        {/* Sekcija sa dodatnim informacijama */}
        <div className="about-section">
          <h3>O ordinaciji</h3>
          <p>
            Ordinacija psihologa pruža podršku za različite izazove, uključujući
            anksioznost, stres, porodične odnose i još mnogo toga. Terapije su
            dostupne uživo i online.
          </p>
        </div>

        {/* Dugmad za prijavu i registraciju */}
        <div className="action-buttons">
          <Link to="/login" className="btn btn-primary">
            Prijava
          </Link>
          <Link to="/signup" className="btn btn-secondary">
            Registracija
          </Link>
        </div>
      </div>
    </>
  );
};

export default Home;
