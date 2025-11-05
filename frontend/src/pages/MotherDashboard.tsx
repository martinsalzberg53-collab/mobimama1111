import { useUser } from "../context/UserContext";
import AppointmentCard from "../components/AppointmentCard"; // Import new card
import AITipsCard from "../components/AITipsCard"; // Import new card
import QuickActionsCard from "../components/QuickActionsCard"; // Import new card
import "../styles/MotherDashboard.css"; // We will use new styles

const MotherDashboard = () => {
  const { user} = useUser();

  return (
    <div className="dashboard-container">
      {/* Header / Greeting */}
      <header className="dashboard-header">
        <div className="header-greeting">
          <h1>Hi, {user?.username}!</h1>
          <p>Welcome to your Mobi Mama dashboard</p>
        </div>
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