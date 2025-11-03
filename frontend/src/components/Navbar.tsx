import { Link } from "react-router-dom";
import { useUser } from "../context/UserContext";
import "../styles/Navbar.css";

const Navbar = () => {
  const { user, logout } = useUser();

  return (
    <nav>
      <div>
        <Link to="/" className="brand">
          MyApp
        </Link>
      </div>

      <div className="links">
        {user ? (
          <>
            <span style={{ marginRight: "10px" }}>Hi, {user.username}</span>

            {/* Role-based dashboard links */}
            {user.role === "mother" && (
              <Link to="/dashboard/mother" style={{ marginRight: "10px" }}>
                Mother Dashboard
              </Link>
            )}

            {user.role === "nurse" && (
              <Link to="/dashboard/nurse" style={{ marginRight: "10px" }}>
                Nurse Dashboard
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
