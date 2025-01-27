
import { Link } from "react-router-dom";
import "../styles/Home.css";
import { FaBrain, FaHandsHelping, FaSmile, FaLaptop } from "react-icons/fa";
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from "react-icons/fa";

const Home = () => {
  return (
    <>
      <div className="home-container">
        {/* Intro sekcija */}
        <div className="intro-section">
          <img
            src="src/photos/psiholoskinja.png"
            alt="Ana Jovanović"
            className="intro-image"
          />
          <h2>Dr. Ana Jovanović</h2>
          <p>
            Specijalista za individualnu, grupnu i porodičnu terapiju. Sa preko
            10 godina iskustva, Ana je posvećena pružanju vrhunske psihološke
            podrške.
          </p>
          <div className="buttons-container">
            <Link to="/login" className="btn-primary">
              Prijava
            </Link>
            <Link to="/register" className="btn-secondary">
              Registracija
            </Link>
          </div>
        </div>

        {/* Sekcija sa ikonama */}
        <div className="features-section">
          <h3>Naša misija</h3>
          <div className="features-cards">
            <div className="card">
              <FaBrain className="icon" />
              <h4>Mentalno zdravlje</h4>
              <p>
                Pomažemo vam da prevaziđete izazove i poboljšate svoje mentalno
                blagostanje.
              </p>
            </div>
            <div className="card">
              <FaHandsHelping className="icon" />
              <h4>Podrška</h4>
              <p>
                Pružamo individualnu i grupnu podršku u skladu sa vašim
                potrebama.
              </p>
            </div>
            <div className="card">
              <FaSmile className="icon" />
              <h4>Pozitivan pristup</h4>
              <p>
                Koristimo metode koje podstiču rast, optimizam i unutrašnju
                snagu.
              </p>
            </div>
            <div className="card">
              <FaLaptop className="icon" />
              <h4>Online terapije</h4>
              <p>
                Dostupni smo i online, pružajući terapiju u udobnosti vašeg
                doma.
              </p>
            </div>
          </div>
        </div>

        {/* Sekcija sa iskustvima korisnika */}
        <div className="testimonials-section">
          <h3>Naši klijenti</h3>
          <div className="testimonials">
            <div className="testimonial">
              <p>
                "Dr. Ana mi je pomogla da pronađem mir u teškim trenucima. Hvala
                na svemu!"
              </p>
              <span>- Marija</span>
            </div>
            <div className="testimonial">
              <p>
                "Izuzetno profesionalan i topao pristup. Preporučujem svakome."
              </p>
              <span>- Marko</span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="footer">
          <div className="footer-content">
            <div className="footer-left">
              <p>© 2025 Ordinacija psihologa. Sva prava zadržana.</p>
              <p>Kontakt: +382 67 123 456 | anapsiholog@gmail.com</p>
            </div>
            <div className="footer-center">
              <h4>Pretplatite se na naš newsletter</h4>
              <input type="email" placeholder="Unesite vaš email" />
              <button>Pretplati se</button>
            </div>
            <div className="footer-right">
              <h4>Pratite nas</h4>
              <div className="social-icons">
                <a
                  href="https://www.facebook.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  <FaFacebook />
                </a>
                <a
                  href="https://www.twitter.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  <FaTwitter />
                </a>
                <a
                  href="https://www.instagram.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  <FaInstagram />
                </a>
                <a
                  href="https://www.linkedin.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  <FaLinkedin />
                </a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
};

export default Home;
