import { useUser } from "../context/UserContext";
import AppointmentCard from "../components/AppointmentCard";
import AITipsCard from "../components/AITipsCard";
import QuickActionsCard from "../components/QuickActionsCard";
import "../styles/MotherDashboard.css";
import { useNavigate } from "react-router-dom"; // 1. Import useNavigate

const MotherDashboard = () => {
  // 2. Get 'logout' from context, and 'first_name' from user
  const { user, logout } = useUser();
  const navigate = useNavigate(); // 3. Initialize navigate

  const handleLogout = () => {
    logout();
    navigate("/login"); // Redirect to login after logout
  };

  if (!user || user.role !== "MOTHER") {
    return (
      <div className="mother-dashboard-container">
        <h1>Access denied</h1>
        <p>This page is only available to mothers.</p>
      </div>
    );
  }

  return (
    <div className="mother-dashboard-container aurora-bg">
      <header className="mother-hero">
        <div className="mother-hero-copy">
          <span className="eyebrow">Mobi Mama</span>
          <h1>
            Hi, <span className="gradient-text">{user.first_name}</span>!
          </h1>
          <p>
            Your pregnancy journey, appointments and health tips in one place.
          </p>
        </div>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </header>

      <main className="mother-dashboard-grid">
        <AppointmentCard />
        <AITipsCard />
        <QuickActionsCard />
      </main>
    </div>
  );
};

export default MotherDashboard;