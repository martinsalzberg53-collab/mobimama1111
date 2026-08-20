import React, { useEffect, useState } from "react";
import API from "../api/axios";
import { useUser } from "../context/UserContext";
import "../styles/NurseProfile.css";

type Assignment = {
  id: number;
  nurse: number;
  clinic: number;
};

type Clinic = {
  id: number;
  name: string;
  address: string;
  phone_number: string;
};

type MotherProfile = {
  id: number;
  user: {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
  };
  risk_level: string;
  risk_reasons: string[];
  due_date: string | null;
  phone_number: string | null;
  clinic_name: string | null;
};

const NurseProfile = () => {
  const { user, token, login } = useUser();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [assignment, setAssignment] = useState<Assignment | null>(null);
  const [clinic, setClinic] = useState<Clinic | null>(null);
  const [patients, setPatients] = useState<MotherProfile[]>([]);
  const [saveMsg, setSaveMsg] = useState("");
  const [saveError, setSaveError] = useState("");

  useEffect(() => {
    if (user) {
      setFirstName(user.first_name || "");
      setLastName(user.last_name || "");
    }
    fetchAssignment();
    fetchPatients();
  }, [user]);

  const fetchAssignment = async () => {
    try {
      const res = await API.get<Assignment[]>("/clinics/nurse-assignments/");
      const a = res.data[0];
      if (a) {
        setAssignment(a);
        const clinicsRes = await API.get<Clinic[]>("/clinics/clinics/");
        const matched = clinicsRes.data.find((c) => c.id === a.clinic);
        if (matched) setClinic(matched);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchPatients = async () => {
    try {
      const res = await API.get<MotherProfile[]>("/mothers/profiles/");
      setPatients(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const saveName = async () => {
    setSaveMsg("");
    setSaveError("");
    try {
      const res = await API.patch("/users/profile/", {
        first_name: firstName,
        last_name: lastName,
      });
      if (login && token) login({ ...user!, ...res.data }, token);
      setSaveMsg("Profile updated.");
    } catch (err: any) {
      console.error(err);
      setSaveError(err.response?.data?.detail || "Could not save changes.");
    }
  };

  const fullName =
    `${user?.first_name || ""} ${user?.last_name || ""}`.trim() || "Not set";

  return (
    <div className="nurse-profile-container">
      <div className="nurse-profile-header">
        <h1>My Profile</h1>
      </div>

      <div className="nurse-profile-card">
        {/* --- Account --- */}
        <h3 className="nurse-section-header">Account Details</h3>
        <div className="nurse-field">
          <span className="nurse-label">Email:</span>
          <span className="nurse-value">{user?.email}</span>
        </div>
        <div className="nurse-field">
          <span className="nurse-label">Role:</span>
          <span className="nurse-value">{user?.role}</span>
        </div>

        {/* --- Personal --- */}
        <h3 className="nurse-section-header">Personal Details</h3>
        <div className="nurse-field">
          <span className="nurse-label">Full name:</span>
          <span className="nurse-value">{fullName}</span>
        </div>

        <label className="nurse-field">
          <span className="nurse-label">First name:</span>
          <input
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />
        </label>
        <label className="nurse-field">
          <span className="nurse-label">Last name:</span>
          <input
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />
        </label>
        <button className="nurse-save-button" onClick={saveName}>
          Save Name
        </button>
        {saveMsg && <p className="nurse-success">{saveMsg}</p>}
        {saveError && <p className="nurse-error">{saveError}</p>}

        {/* --- Clinic --- */}
        <h3 className="nurse-section-header">Assigned Clinic</h3>
        {clinic ? (
          <div className="nurse-field">
            <span className="nurse-label">Clinic:</span>
            <span className="nurse-value">{clinic.name}</span>
          </div>
        ) : (
          <p className="nurse-empty-text">
            No clinic assigned yet. Set your clinic on the{" "}
            <a href="/NurseDashboard">Dashboard</a>.
          </p>
        )}

        {/* --- Assigned Patients --- */}
        <h3 className="nurse-section-header">
          Assigned Patients ({patients.length})
        </h3>
        {patients.length ? (
          <div className="nurse-patient-list">
            {patients.map((p) => (
              <div key={p.id} className="nurse-patient-card">
                <div className="nurse-patient-name">
                  {p.user.first_name} {p.user.last_name}
                </div>
                <div className="nurse-patient-meta">
                  <span className={`nurse-risk-badge ${p.risk_level.toLowerCase()}`}>
                    {p.risk_level}
                  </span>
                  <span>Due: {p.due_date || "Unknown"}</span>
                  <span>Phone: {p.phone_number || "Unknown"}</span>
                </div>
                {p.risk_reasons.length > 0 && (
                  <div className="nurse-patient-reasons">
                    {p.risk_reasons.join("; ")}
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="nurse-empty-text">
            No patients assigned to you yet. Approve a pending appointment on
            the{" "}
            <a href="/NurseDashboard">Dashboard</a>{" "}
            to take on a patient.
          </p>
        )}
      </div>
    </div>
  );
};

export default NurseProfile;
