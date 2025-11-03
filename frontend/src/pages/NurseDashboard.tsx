import React from "react";
import { useUser } from "../context/UserContext";
import "../styles/NurseDashboard.css"; // import your dashboard-specific CSS

const NurseDashboard = () => {
  const { user } = useUser();

  return (
    <div className="dashboard-container">
      <h1>Nurse Dashboard</h1>
      <p>Welcome, {user?.username}!</p>
      <p>This is where nurse-specific features will be displayed.</p>
    </div>
  );
};

export default NurseDashboard;
