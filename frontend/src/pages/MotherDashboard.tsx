import React from "react";
import { useUser } from "../context/UserContext";
import "../styles/MotherDashboard.css";

const MotherDashboard = () => {
  const { user, logout } = useUser();

  // Mock upcoming appointments
  const appointments = [
    { date: "2025-11-05", time: "10:00 AM", clinic: "Accra Health Clinic" },
    { date: "2025-11-12", time: "2:00 PM", clinic: "Korle Bu Clinic" },
  ];

  // Mock AI health tips
  const aiTips = [
    "Drink 8 glasses of water daily to stay hydrated.",
    "Prenatal vitamins improve baby health.",
    "Take a 15-minute walk daily for circulation.",
  ];

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Hi, {user?.username}</h1>
        <p>Welcome to your Mobi Mama dashboard</p>
        <button onClick={logout} className="logout-btn">Logout</button>
      </header>

      <section className="profile-card">
        <h2>Your Profile</h2>
        <p><strong>Email:</strong> {user?.email}</p>
        <p><strong>Role:</strong> {user?.role}</p>
        <p><strong>Clinic:</strong> {user?.clinic || "Not assigned"}</p>
      </section>

      <section className="appointments-card">
        <h2>Upcoming Appointments</h2>
        {appointments.length > 0 ? (
          <ul>
            {appointments.map((appt, index) => (
              <li key={index}>
                {appt.date} at {appt.time} - {appt.clinic}
              </li>
            ))}
          </ul>
        ) : (
          <p>No upcoming appointments</p>
        )}
      </section>

      <section className="ai-tips-card">
        <h2>AI Health Tips</h2>
        <ul>
          {aiTips.map((tip, index) => (
            <li key={index}>{tip}</li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default MotherDashboard;
