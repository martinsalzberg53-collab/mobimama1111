import { Link } from "react-router-dom";
import { useUser } from "../context/UserContext";
import "../styles/Navbar.css";

const Navbar = () => {
  const { user, logout } = useUser();

  return (
    <nav>
      <div>
        <Link to="/" className="brand">
          Mobi
        </Link>
      </div>

      <div className="links">
        {user ? (
          <>
            <span style={{ marginRight: "10px" }}>Hi, {user.username}</span>

            {/* Role-based dashboard links */}
            {user.role === "mother" && (
              <Link to="/motherdashboard" style={{ marginRight: "10px" }}>
                My Dashboard
              </Link>
            )}

            {user.role === "nurse" && (
              <Link to="/nursedashboard" style={{ marginRight: "10px" }}>
                My Dashboard
              </Link>
            )}

            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
