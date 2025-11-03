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
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
