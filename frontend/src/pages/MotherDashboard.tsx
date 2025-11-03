import React from "react";
import { useUser } from "../context/UserContext";
import "../styles/MotherDashboard.css"; // import your dashboard-specific CSS

const MotherDashboard = () => {
  const { user } = useUser();

  return (
    <div className="dashboard-container">
      <h1>Mother Dashboard</h1>
      <p>Welcome, {user?.username}!</p>
      <p>This is where mother-specific features will be displayed.</p>
    </div>
  );
};

export default MotherDashboard;
