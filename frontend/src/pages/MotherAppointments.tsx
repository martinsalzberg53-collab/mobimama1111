import React, { useEffect, useState } from "react";
import { useUser } from "../context/UserContext";
import API from "../api/axios";
import "../styles/MotherAppointments.css";

type Clinic = {
  id: number;
  name: string;
  address: string;
  phone_number: string;
};

type Appointment = {
  id: number;
  mother: number;
  nurse: number | null;
  clinic_name: number | null;
  date_time: string;
  reason: string;
  status: string;
};

const MotherAppointments = () => {
  const { user } = useUser();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [clinics, setClinics] = useState<Clinic[]>([]);
  const [selectedClinic, setSelectedClinic] = useState<number | null>(null);
  const [dateTime, setDateTime] = useState("");
  const [reason, setReason] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAppointments();
    fetchClinics();
  }, []);

  const fetchAppointments = async () => {
    try {
      const response = await API.get<Appointment[]>("/appointments/appointments/");
      setAppointments(response.data);
    } catch (err) {
      console.error(err);
      setError("Unable to load appointments. Please refresh.");
    }
  };

  const fetchClinics = async () => {
    try {
      const response = await API.get<Clinic[]>("/clinics/clinics/");
      setClinics(response.data);
      if (response.data.length && selectedClinic === null) {
        setSelectedClinic(response.data[0].id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");
    setSuccess("");

    if (!selectedClinic || !dateTime) {
      setError("Please choose a clinic and appointment date/time.");
      return;
    }

    try {
      await API.post("/appointments/appointments/", {
        clinic_name: selectedClinic,
        date_time: dateTime,
        reason,
      });
      setSuccess("Appointment booked successfully.");
      setReason("");
      setDateTime("");
      fetchAppointments();
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "Could not book appointment.");
    }
  };

  const upcoming = appointments.filter((appt) => appt.status !== "cancelled");

  return (
    <div className="appointments-container">
      <header className="appointments-header">
        <div>
          <h1>My Appointments</h1>
          <p>Book a follow-up appointment and review your upcoming care.</p>
        </div>
      </header>

      <section className="booking-panel">
        <div className="booking-card">
          <h2>Book an Appointment</h2>
          <form onSubmit={handleSubmit} className="booking-form">
            <label>
              Choose a hospital
              <select
                value={selectedClinic ?? ""}
                onChange={(e) => setSelectedClinic(Number(e.target.value))}
                required
              >
                <option value="" disabled>
                  Select a hospital
                </option>
                {clinics.map((clinic) => (
                  <option key={clinic.id} value={clinic.id}>
                    {clinic.name}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Date & time
              <input
                type="datetime-local"
                value={dateTime}
                onChange={(e) => setDateTime(e.target.value)}
                required
              />
            </label>

            <label>
              Reason for visit
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="Describe your reason for the follow-up"
              />
            </label>

            {error && <p className="form-error">{error}</p>}
            {success && <p className="form-success">{success}</p>}

            <button type="submit" className="submit-button">
              Book Appointment
            </button>
          </form>
        </div>

        <div className="clinic-list-card">
          <h2>Hospitals Near You</h2>
          <div className="clinic-list">
            {clinics.length > 0 ? (
              clinics.map((clinic) => (
                <div className="clinic-card" key={clinic.id}>
                  <h3>{clinic.name}</h3>
                  <p>{clinic.address}</p>
                  <p>{clinic.phone_number}</p>
                </div>
              ))
            ) : (
              <p>No hospitals available yet.</p>
            )}
          </div>
        </div>
      </section>

      <section className="appointments-list-section">
        <h2>Upcoming Appointments</h2>
        {upcoming.length ? (
          <ul className="appointments-list">
            {upcoming.map((appointment) => (
              <li className="appointment-card" key={appointment.id}>
                <span className="appointment-date">
                  {new Date(appointment.date_time).toLocaleString()}
                </span>
                <span className="appointment-status">Status: {appointment.status}</span>
                <p className="appointment-reason">{appointment.reason}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="appointments-empty">No appointments booked yet.</p>
        )}
      </section>
    </div>
  );
};

export default MotherAppointments;
