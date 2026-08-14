import React, { useEffect, useState } from "react";
import API from "../api/axios";
import { useUser } from "../context/UserContext";
import "../styles/NurseDashboard.css";

type UserSummary = {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
};

type MotherProfile = {
  id: number;
  user: UserSummary;
  due_date: string | null;
  clinic_name: string | null;
  health_info: Record<string, any>;
  ai_insights: Record<string, any>;
  phone_number: string | null;
  risk_level: "Low" | "Medium" | "High";
  risk_reasons: string[];
};

type Clinic = {
  id: number;
  name: string;
  address: string;
  phone_number: string;
};

const NurseDashboard = () => {
  const { user } = useUser();
  const [mothers, setMothers] = useState<MotherProfile[]>([]);
  const [clinics, setClinics] = useState<Clinic[]>([]);
  const [myAssignment, setMyAssignment] = useState<{ id: number; clinic: number } | null>(null);
  const [selectedClinic, setSelectedClinic] = useState<number | null>(null);
  const [assignmentMsg, setAssignmentMsg] = useState("");
  const [assignmentError, setAssignmentError] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAssignedMothers();
    fetchClinics();
    fetchMyAssignment();
  }, []);

  const fetchAssignedMothers = async () => {
    try {
      const response = await API.get<MotherProfile[]>("/mothers/profiles/");
      setMothers(response.data);
      // keep mothers loaded for nurse view
    } catch (err) {
      console.error(err);
      setError("Unable to load assigned mothers. Please refresh.");
    }
  };

  const fetchClinics = async () => {
    try {
      const response = await API.get<Clinic[]>("/clinics/clinics/");
      setClinics(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchMyAssignment = async () => {
    try {
      const response = await API.get<{ id: number; nurse: number; clinic: number }[]>(
        "/clinics/nurse-assignments/"
      );
      const assignment = response.data[0];
      setMyAssignment(assignment ? { id: assignment.id, clinic: assignment.clinic } : null);
      setSelectedClinic(assignment ? assignment.clinic : null);
    } catch (err) {
      console.error(err);
    }
  };

  const saveAssignment = async () => {
    setAssignmentMsg("");
    setAssignmentError("");

    if (!selectedClinic) {
      setAssignmentError("Please choose your clinic first.");
      return;
    }

    try {
      if (myAssignment) {
        await API.put(`/clinics/nurse-assignments/${myAssignment.id}/`, {
          clinic: selectedClinic,
        });
      } else {
        await API.post("/clinics/nurse-assignments/", {
          clinic: selectedClinic,
        });
      }
      setAssignmentMsg("Your clinic assignment was saved.");
      fetchMyAssignment();
    } catch (err: any) {
      console.error(err);
      const detail =
        err.response?.data?.detail ||
        err.response?.data?.non_field_errors?.[0] ||
        "Could not save your clinic assignment.";
      setAssignmentError(detail);
    }
  };

  const highRiskMothers = mothers.filter((mother) => mother.risk_level === "High");

  const getBadgeClass = (risk: MotherProfile["risk_level"]) => {
    switch (risk) {
      case "High":
        return "risk-badge high";
      case "Medium":
        return "risk-badge medium";
      default:
        return "risk-badge low";
    }
  };

  if (!user || user.role !== "NURSE") {
    return (
      <div className="nurse-dashboard-container">
        <h1>Access denied</h1>
        <p>This page is only available to nurses.</p>
      </div>
    );
  }

  return (
    <div className="nurse-dashboard-container">
      <header className="dashboard-header">
        <div>
          <h1>Welcome, {user.first_name}</h1>
          <p>Your assigned patients and clinical alerts are shown below.</p>
        </div>
        <div className="notification-summary">
          <span className="notification-count">{highRiskMothers.length}</span>
          <p>High-risk mothers require attention</p>
        </div>
      </header>

      <section className="alerts-panel">
        <h2>My Clinic</h2>
        {clinics.length ? (
          <>
            <label htmlFor="my-clinic">Select the clinic where you work</label>
            <select
              id="my-clinic"
              value={selectedClinic ?? ""}
              onChange={(e) => setSelectedClinic(Number(e.target.value))}
            >
              <option value="" disabled>
                Choose a clinic
              </option>
              {clinics.map((clinic) => (
                <option key={clinic.id} value={clinic.id}>
                  {clinic.name}
                </option>
              ))}
            </select>
            <button onClick={saveAssignment} className="save-assignment-button">
              Save Clinic
            </button>
            {assignmentMsg && <p className="assignment-success">{assignmentMsg}</p>}
            {assignmentError && <p className="assignment-error">{assignmentError}</p>}
          </>
        ) : (
          <p className="alerts-empty">No clinics are available yet.</p>
        )}
      </section>

      <section className="alerts-panel">
        <h2>Automated Safety Alerts</h2>
        {highRiskMothers.length ? (
          highRiskMothers.map((mother) => (
            <div key={mother.id} className="alert-card">
              <div className="alert-title">
                <strong>{mother.user.first_name} {mother.user.last_name}</strong>
                <span className="alert-risk">{mother.risk_level}</span>
              </div>
              <p>{mother.clinic_name || "Unassigned clinic"}</p>
              <ul>
                {mother.risk_reasons.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </div>
          ))
        ) : (
          <p className="alerts-empty">No active high-risk alerts right now.</p>
        )}
      </section>

      <section className="mother-grid-section">
        <h2>Assigned Patients</h2>
        <div className="mother-grid">
          {mothers.map((mother) => (
            <div key={mother.id} className="mother-card">
              <div className="mother-card-header">
                <h3>{mother.user.first_name} {mother.user.last_name}</h3>
                <span className={getBadgeClass(mother.risk_level)}>{mother.risk_level}</span>
              </div>
              <p><strong>Clinic:</strong> {mother.clinic_name || "Not assigned"}</p>
              <p><strong>Due:</strong> {mother.due_date || "Unknown"}</p>
              <p><strong>Phone:</strong> {mother.phone_number || "Unknown"}</p>
              <p className="health-info-label">Latest indicators:</p>
              <div className="health-info-grid">
                {Object.entries(mother.health_info || {}).map(([key, value]) => (
                  <div key={key} className="health-info-item">
                    <span className="health-info-key">{key.replace(/_/g, " ")}</span>
                    <strong>{String(value)}</strong>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="hospital-list-section">
        <h2>Hospital Network</h2>
        <div className="hospital-list">
          {clinics.length ? (
            clinics.map((clinic) => (
              <div key={clinic.id} className="hospital-card">
                <h3>{clinic.name}</h3>
                <p>{clinic.address}</p>
                <p>{clinic.phone_number}</p>
              </div>
            ))
          ) : (
            <p className="alerts-empty">No hospitals available yet.</p>
          )}
        </div>
      </section>
    </div>
  );
};

export default NurseDashboard;
