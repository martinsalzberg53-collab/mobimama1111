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

  return (
    // 4. Use the non-conflicting CSS class name
    <div className="mother-dashboard-container">
      {/* Header / Greeting */}
      <header className="dashboard-header">
        <div className="header-greeting">
          {/* 5. Use user.first_name, not username */}
          <h1>Hi, {user?.first_name}!</h1>
          <p>Welcome to your Mobi Mama dashboard</p>
        </div>
        {/* 6. Re-add the logout button */}
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </header>

      {/* Main Sections - Now a responsive grid */}
      <main className="dashboard-grid">
        <AppointmentCard />
        <AITipsCard />
        <QuickActionsCard />
      </main>
    </div>
  );
};

export default MotherDashboard;