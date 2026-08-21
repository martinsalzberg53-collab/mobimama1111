import React from "react";
import { Link } from "react-router-dom";
import "../styles/MotherDashboard.css";

const QuickActionsCard = () => {
  return (
    <section className="dashboard-card quick-actions-card">
      <h2>Quick Actions</h2>
      <div className="buttons-container">
        {/* I've added a link to your Mobi chatbot here */}
        <Link to="/chat" className="action-btn chat-btn">
          Chat with Mobi
        </Link>
        <Link to="/motherprofile" className="action-btn">
          My Profile
        </Link>
        <Link to="/motherappointments" className="action-btn">
          All Appointments
        </Link>
        <Link to="/symptom-tracker" className="action-btn">
          Track Symptoms
        </Link>
      </div>
    </section>
  );
};

export default QuickActionsCard;