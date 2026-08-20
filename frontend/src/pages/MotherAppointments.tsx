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

type MotherProfile = {
  id: number;
  phone_number: string | null;
  due_date: string | null;
};

type Appointment = {
  id: number;
  clinic_name: number | null;
  date_time: string;
  reason: string;
  status: string;
  clinic_display: string;
};

const MotherAppointments = () => {
  const { user } = useUser();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [clinics, setClinics] = useState<Clinic[]>([]);
  const [profile, setProfile] = useState<MotherProfile | null>(null);
  const [selectedClinic, setSelectedClinic] = useState<number | null>(null);
  const [dateTime, setDateTime] = useState("");
  const [reason, setReason] = useState("");
  const [phone, setPhone] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAppointments();
    fetchClinics();
    fetchProfile();
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

  const fetchProfile = async () => {
    try {
      const response = await API.get<MotherProfile[]>("/mothers/profiles/");
      const p = response.data[0];
      if (p) {
        setProfile(p);
        setPhone(p.phone_number || "");
        setDueDate(p.due_date || "");
      }
    } catch {
      // Profile doesn't exist yet; will be created on first booking.
    }
  };

  const saveProfile = async () => {
    if (profile) {
      await API.patch(`/mothers/profiles/${profile.id}/`, {
        phone_number: phone,
        due_date: dueDate || null,
      });
    } else {
      const res = await API.post("/mothers/profiles/", {
        phone_number: phone,
        due_date: dueDate || null,
      });
      setProfile(res.data);
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

    if (!phone.trim()) {
      setError("Please enter your phone number so the nurse can contact you.");
      return;
    }

    try {
      await saveProfile();
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
      const data = err.response?.data;
      let msg = "Could not book appointment.";
      if (typeof data === "string") {
        msg = data;
      } else if (data && typeof data === "object") {
        if (data.detail) {
          msg = data.detail;
        } else {
          const parts = Object.entries(data).map(([key, value]) => {
            const text = Array.isArray(value) ? value.join(", ") : String(value);
            return `${key}: ${text}`;
          });
          if (parts.length) msg = parts.join("; ");
        }
      }
      setError(msg);
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
              Phone number
              <input
                type="tel"
                value={phone}
                placeholder="e.g. 024 000 0000"
                onChange={(e) => setPhone(e.target.value)}
                required
              />
            </label>

            <label>
              Due date
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
              />
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
                <span className="appointment-clinic">
                  {appointment.clinic_display || "Unknown clinic"}
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
