import React, { useState, useEffect } from "react";
import "../styles/MotherDashboard.css"; // Uses the same stylesheet

const AppointmentCard = () => {
  const [appointment, setAppointment] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Simulate fetching data from an API
  useEffect(() => {
    const fetchAppointment = () => {
      // Mock data
      const mockAppointment = {
        date: "2025-11-10",
        time: "10:30 AM",
        clinic: "Accra Maternal Health Clinic",
        doctor: "Dr. Bempah",
      };

      // Simulate network delay
      setTimeout(() => {
        setAppointment(mockAppointment);
        setIsLoading(false);
      }, 1500); // 1.5 second delay
    };

    fetchAppointment();
  }, []);

  // Helper to format the date
  const formattedDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <section className="dashboard-card appointment-card">
      <h2>Next Appointment</h2>
      {isLoading ? (
        <p>Loading appointment...</p>
      ) : appointment ? (
        <div className="appointment-details">
          <p className="appointment-date">
            {formattedDate(appointment.date)}
          </p>
          <p className="appointment-time">
            {appointment.time}
          </p>
          <p className="appointment-location">
            {appointment.clinic} (with {appointment.doctor})
          </p>
        </div>
      ) : (
        <p>No upcoming appointments found.</p>
      )}
    </section>
  );
};

export default AppointmentCard;