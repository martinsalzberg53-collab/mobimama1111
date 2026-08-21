import React, { useEffect, useState } from "react";
import API from "../api/axios";
import { useUser } from "../context/UserContext";
import "../styles/MotherProfile.css";

type MotherProfile = {
  id: number;
  due_date: string | null;
  clinic_name: string | null;
  health_info: Record<string, any>;
  phone_number: string | null;
  risk_level: string;
  risk_reasons: string[];
};

type Clinic = {
  id: number;
  name: string;
  address: string;
  phone_number: string;
};

const MotherProfile = () => {
  const { user } = useUser();
  const [profile, setProfile] = useState<MotherProfile | null>(null);
  const [clinics, setClinics] = useState<Clinic[]>([]);
  const [dueDate, setDueDate] = useState("");
  const [phone, setPhone] = useState("");
  const [clinicName, setClinicName] = useState("");
  const [saveMsg, setSaveMsg] = useState("");
  const [saveError, setSaveError] = useState("");

  useEffect(() => {
    fetchProfile();
    fetchClinics();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await API.get<MotherProfile[]>("/mothers/profiles/");
      const p = response.data[0];
      if (p) {
        setProfile(p);
        setDueDate(p.due_date || "");
        setPhone(p.phone_number || "");
        setClinicName(p.clinic_name || "");
      }
    } catch (err) {
      console.error(err);
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

  const saveProfile = async () => {
    setSaveMsg("");
    setSaveError("");
    if (!profile) return;
    try {
      await API.patch(`/mothers/profiles/${profile.id}/`, {
        due_date: dueDate || null,
        phone_number: phone,
        clinic_name: clinicName,
      });
      setSaveMsg("Profile updated and visible to your nurse.");
      fetchProfile();
    } catch (err: any) {
      console.error(err);
      setSaveError(
        err.response?.data?.detail || "Could not save your profile."
      );
    }
  };

  if (!user) {
    return (
      <div className="mother-profile-container">
        <h1>Loading Profile...</h1>
      </div>
    );
  }

  const fullName = `${user.first_name || ""} ${user.last_name || ""}`.trim();
  const indicators = profile?.health_info || {};
  const symptoms: string[] = indicators.symptoms || [];

  return (
    <div className="mother-profile-container">
      <div className="profile-header">
        <h1>My Profile</h1>
      </div>

      <div className="profile-card">
        <h3 className="profile-section-header">Account Details</h3>
        <div className="profile-field">
          <span className="label">Email:</span>
          <span className="value">{user.email}</span>
        </div>
        <div className="profile-field">
          <span className="label">Account Type:</span>
          <span className="value">{user.role}</span>
        </div>

        <h3 className="profile-section-header">Personal Details</h3>
        <div className="profile-field">
          <span className="label">Full Name:</span>
          <span className="value">{fullName || "Not set"}</span>
        </div>

        <h3 className="profile-section-header">Health Details</h3>

        <label className="profile-field">
          <span className="label">Due Date:</span>
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
          />
        </label>

        <label className="profile-field">
          <span className="label">Phone Number:</span>
          <input
            type="tel"
            value={phone}
            placeholder="e.g. 024 000 0000"
            onChange={(e) => setPhone(e.target.value)}
          />
        </label>

        <label className="profile-field">
          <span className="label">Preferred Clinic:</span>
          <select
            value={clinicName}
            onChange={(e) => setClinicName(e.target.value)}
          >
            <option value="">Not assigned</option>
            {clinics.map((clinic) => (
              <option key={clinic.id} value={clinic.name}>
                {clinic.name}
              </option>
            ))}
          </select>
        </label>

        <button className="profile-save-button" onClick={saveProfile}>
          Save Profile
        </button>
        {saveMsg && <p className="profile-success">{saveMsg}</p>}
        {saveError && <p className="profile-error">{saveError}</p>}

        {profile && (
          <>
            <h3 className="profile-section-header">Risk & Latest Indicators</h3>
            <div className="profile-field">
              <span className="label">Risk Level:</span>
              <span className="value">{profile.risk_level}</span>
            </div>
            {profile.risk_reasons.length > 0 && (
              <div className="profile-field">
                <span className="label">Reasons:</span>
                <span className="value">
                  {profile.risk_reasons.join("; ")}
                </span>
              </div>
            )}
            {symptoms.length > 0 && (
              <div className="profile-field">
                <span className="label">Reported Symptoms:</span>
                <span className="value">
                  {symptoms.join(", ").replace(/_/g, " ")}
                </span>
              </div>
            )}
            {indicators.fetal_movement && (
              <div className="profile-field">
                <span className="label">Fetal Movement:</span>
                <span className="value">{indicators.fetal_movement}</span>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default MotherProfile;
