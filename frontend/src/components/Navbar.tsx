import { Link, NavLink, useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import "../styles/Navbar.css";

// Helper function to handle active NavLink styling
// This will add the class "active-link" to the NavLink that matches the current URL
const getNavLinkClass = ({ isActive }: { isActive: boolean }) => {
  return isActive ? "nav-link active-link" : "nav-link";
};

const Navbar = () => {
  const { user, logout } = useUser();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login"); // Redirect to login page after logout
  };

  // --- Links for Logged-Out Users ---
  const guestLinks = (
    <>
      <NavLink to="/login" className={getNavLinkClass}>
        Login
      </NavLink>
      <NavLink to="/register" className="nav-link cta-button">
        Sign Up
      </NavLink>
    </>
  );

  // --- Links for "Mother" Role ---
  const motherLinks = (
    <>
      <NavLink to="/MotherDashboard" className={getNavLinkClass}>
        Dashboard
      </NavLink>
      <NavLink to="/motherprofile" className={getNavLinkClass}>
        Profile
      </NavLink>
      <NavLink to="/motherappointments" className={getNavLinkClass}>
        Appointments
      </NavLink>
    </>
  );

  // --- Links for "Nurse" Role ---
  const nurseLinks = (
    <>
      <NavLink to="/NurseDashboard" className={getNavLinkClass}>
        Dashboard
      </NavLink>
      <NavLink to="/nurse-profile" className={getNavLinkClass}>
        Profile
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
            {/* We use user.first_name, which we get from our API */}
            <span className="navbar-greeting">Hi, {user.first_name}!</span>

            {/* Render links based on user role */}
            {user.role === "MOTHER" && motherLinks}
            {user.role === "NURSE" && nurseLinks}

            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </>
        ) : (
          guestLinks
        )}
      </div>
    </nav>
  );
};

export default Navbar;