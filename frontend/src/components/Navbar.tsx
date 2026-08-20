import { Link, NavLink, useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import { useLanguage } from "../context/LanguageContext";
import "../styles/Navbar.css";

const getNavLinkClass = ({ isActive }: { isActive: boolean }) => {
  return isActive ? "nav-link active-link" : "nav-link";
};

const Navbar = () => {
  const { user, logout } = useUser();
  const { t, language, setLanguage, languages } = useLanguage();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const guestLinks = (
    <>
      <NavLink to="/login" className={getNavLinkClass}>
        {t("nav.login")}
      </NavLink>
      <NavLink to="/register" className="nav-link cta-button">
        {t("nav.signUp")}
      </NavLink>
    </>
  );

  const motherLinks = (
    <>
      <NavLink to="/MotherDashboard" className={getNavLinkClass}>
        {t("nav.dashboard")}
      </NavLink>
      <NavLink to="/motherprofile" className={getNavLinkClass}>
        {t("nav.profile")}
      </NavLink>
      <NavLink to="/motherappointments" className={getNavLinkClass}>
        {t("nav.appointments")}
      </NavLink>
    </>
  );

  const nurseLinks = (
    <>
      <NavLink to="/NurseDashboard" className={getNavLinkClass}>
        {t("nav.dashboard")}
      </NavLink>
      <NavLink to="/nurse-profile" className={getNavLinkClass}>
        {t("nav.profile")}
      </NavLink>
    </>
  );

  return (
    <nav className="navbar-container">
      <div className="navbar-brand">
        <Link to={user ? (user.role === 'MOTHER' ? "/MotherDashboard" : "/NurseDashboard") : "/"}>
          Mobi Mama
        </Link>
      </div>

      <div className="navbar-links">
        {user ? (
          <>
            <span className="navbar-greeting">{t("nav.hi")}, {user.first_name}!</span>

            {user.role === "MOTHER" && motherLinks}
            {user.role === "NURSE" && nurseLinks}

            <button onClick={handleLogout} className="logout-button">
              {t("nav.logout")}
            </button>
          </>
        ) : (
          guestLinks
        )}

        <select
          className="language-switcher"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          aria-label="Language"
        >
          {Object.entries(languages).map(([code, { label }]) => (
            <option key={code} value={code}>{label}</option>
          ))}
        </select>
      </div>
    </nav>
  );
};

export default Navbar;
