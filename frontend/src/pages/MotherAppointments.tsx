import React from "react";
import { useUser } from "../context/UserContext";
import { Link } from "react-router-dom";
import "../styles/MotherDashboard.css";

const MotherDashboard = () => {
  const { user, logout } = useUser();

  // Mock next appointment
  const nextAppointment = {
    date: "2025-11-05",
    time: "10:00 AM",
    clinic: "Accra Health Clinic",
  };

  // Mock AI health tips
  const aiTips = [
    "Drink 8 glasses of water daily to stay hydrated.",
    "Take prenatal vitamins every morning.",
    "Go for a 15-minute walk daily for circulation.",
  ];

  return (
    <div className="dashboard-container">
      {/* Header / Greeting */}
      <header className="dashboard-header">
        <h1>Hi, {user?.username}!</h1>
        <p>Welcome to your Mobi Mama dashboard</p>
        <button onClick={logout} className="logout-btn">Logout</button>
      </header>

      {/* Main Sections */}
      <div className="main-sections">
        {/* Next Appointment */}
        <section className="summary-card">
          <h2>Next Appointment</h2>
          {nextAppointment ? (
            <p>
              {nextAppointment.date} at {nextAppointment.time} - {nextAppointment.clinic}
            </p>
          ) : (
            <p>No upcoming appointments</p>
          )}
        </section>

        {/* AI Health Tips */}
        <section className="ai-tips-card">
          <h2>AI Health Tips</h2>
          <ul>
            {aiTips.map((tip, index) => (
              <li key={index}>{tip}</li>
            ))}
          </ul>
        </section>

        {/* Quick Actions */}
        <section className="quick-actions">
          <h2>Quick Actions</h2>
          <div className="buttons-container">
            <Link to="/motherprofile" className="action-btn">Profile</Link>
            <Link to="/motherappointments" className="action-btn">Appointments</Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default MotherDashboard;
