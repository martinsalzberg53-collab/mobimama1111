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

type Appointment = {
  id: number;
  mother: number | null;
  nurse: number | null;
  clinic_name: number | null;
  date_time: string;
  reason: string;
  status: "pending" | "approved" | "cancelled" | "completed";
  mother_name: string;
  nurse_name: string;
  clinic_display: string;
  mother_summary: {
    name: string;
    risk_level: "Low" | "Medium" | "High";
    risk_reasons: string[];
    due_date: string | null;
    phone_number: string | null;
    indicators: Record<string, any>;
  } | null;
};

const NurseDashboard = () => {
  const { user } = useUser();
  const [mothers, setMothers] = useState<MotherProfile[]>([]);
  const [clinics, setClinics] = useState<Clinic[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [apptMsg, setApptMsg] = useState("");
  const [apptError, setApptError] = useState("");
  const [busyApptId, setBusyApptId] = useState<number | null>(null);
  const [myAssignment, setMyAssignment] = useState<{ id: number; clinic: number } | null>(null);
  const [selectedClinic, setSelectedClinic] = useState<number | null>(null);
  const [assignmentMsg, setAssignmentMsg] = useState("");
  const [assignmentError, setAssignmentError] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAssignedMothers();
    fetchClinics();
    fetchMyAssignment();
    fetchAppointments();
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

  const fetchAppointments = async () => {
    try {
      const response = await API.get<Appointment[]>("/appointments/appointments/");
      setAppointments(response.data);
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

  const handleApprove = async (apptId: number) => {
    setApptMsg("");
    setApptError("");
    setBusyApptId(apptId);
    try {
      await API.post(`/appointments/appointments/${apptId}/approve/`);
      setApptMsg("Appointment approved. The mother is now your patient.");
      fetchAppointments();
      fetchAssignedMothers();
    } catch (err: any) {
      console.error(err);
      const detail =
        err.response?.data?.error ||
        err.response?.data?.detail ||
        "Could not approve the appointment.";
      setApptError(detail);
    } finally {
      setBusyApptId(null);
    }
  };

  const handleReject = async (apptId: number) => {
    setApptMsg("");
    setApptError("");
    setBusyApptId(apptId);
    try {
      await API.post(`/appointments/appointments/${apptId}/reject/`);
      setApptMsg("Appointment cancelled.");
      fetchAppointments();
    } catch (err: any) {
      console.error(err);
      const detail =
        err.response?.data?.error ||
        err.response?.data?.detail ||
        "Could not cancel the appointment.";
      setApptError(detail);
    } finally {
      setBusyApptId(null);
    }
  };

  const pendingAppointments = appointments.filter((appt) => appt.status === "pending");

  const formatDateTime = (value: string) => {
    try {
      return new Date(value).toLocaleString();
    } catch {
      return value;
    }
  };

  const getBadgeClass = (risk: MotherProfile["risk_level"]) => {
    return `badge ${risk.toLowerCase()}`;
  };

  if (!user || user.role !== "NURSE") {
    return (
      <div className="nurse-dashboard-container">
        <h1>Access denied</h1>
        <p>This page is only available to nurses.</p>
      </div>
    );
  }

  const activeClinic = clinics.find((clinic) => clinic.id === selectedClinic);

  return (
    <div className="nurse-dashboard-container aurora-bg">
      <header className="nurse-hero">
        <div>
          <span className="eyebrow">Clinical overview</span>
          <h1>
            Welcome, <span className="gradient-text">{user.first_name}</span>
          </h1>
          <p className="nurse-hero-sub">
            Your assigned patients, pending requests and clinical alerts are
            all below.
          </p>
        </div>
      </header>

      <section className="nurse-stats">
        <div className="stat-tile">
          <span className="stat-icon">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M16 19v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="3.2" />
              <path d="M22 19v-2a4 4 0 0 0-3-3.85" />
            </svg>
          </span>
          <span className="stat-body">
            <span className="stat-value">{mothers.length}</span>
            <span className="stat-label">Assigned patients</span>
          </span>
        </div>

        <div className="stat-tile">
          <span className="stat-icon tone-danger">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M10.3 3.6 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.6a2 2 0 0 0-3.4 0Z" />
              <path d="M12 9v4M12 17h.01" />
            </svg>
          </span>
          <span className="stat-body">
            <span className="stat-value">{highRiskMothers.length}</span>
            <span className="stat-label">High-risk alerts</span>
          </span>
        </div>

        <div className="stat-tile">
          <span className="stat-icon tone-warn">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <rect x="3" y="4.5" width="18" height="17" rx="2.5" />
              <path d="M3 9.5h18M8 2.5v4M16 2.5v4" />
            </svg>
          </span>
          <span className="stat-body">
            <span className="stat-value">{pendingAppointments.length}</span>
            <span className="stat-label">Awaiting approval</span>
          </span>
        </div>

        <div className="stat-tile">
          <span className="stat-icon tone-teal">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M3 21h18M5 21V9l7-5.5L19 9v12" />
              <path d="M9.5 21v-5h5v5" />
            </svg>
          </span>
          <span className="stat-body">
            <span className="stat-value">{clinics.length}</span>
            <span className="stat-label">Hospitals in network</span>
          </span>
        </div>
      </section>

      {/* Previously the load error was stored but never rendered, so a failed
          fetch looked identical to "no patients assigned". */}
      {error && <p className="notice notice-error nurse-load-error">{error}</p>}

      <section className="nurse-panel panel">
        <div className="nurse-panel-head">
          <div>
            <span className="eyebrow">Workplace</span>
            <h2>My Clinic</h2>
          </div>
          {activeClinic && <span className="badge approved">{activeClinic.name}</span>}
        </div>

        {activeClinic ? (
          <div className="clinic-picker">
            <p className="nurse-hero-sub">
              You are registered at{" "}
              <strong>{activeClinic.name}</strong>.
            </p>
            <p className="notice notice-success">
              Your hospital was set at registration and cannot be changed here.
            </p>
          </div>
        ) : clinics.length ? (
          <>
            <div className="clinic-picker">
              <label htmlFor="my-clinic">
                Select the clinic where you work
              </label>
              <select
                id="my-clinic"
                className="field"
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
              <button onClick={saveAssignment} className="btn btn-primary">
                Save Clinic
              </button>
            </div>
            {assignmentMsg && <p className="notice notice-success">{assignmentMsg}</p>}
            {assignmentError && <p className="notice notice-error">{assignmentError}</p>}
          </>
        ) : (
          <p className="notice notice-empty">No clinics are available yet.</p>
        )}
      </section>

      <section className="nurse-panel panel">
        <div className="nurse-panel-head">
          <div>
            <span className="eyebrow">Requests</span>
            <h2>Pending Appointments</h2>
          </div>
          {pendingAppointments.length > 0 && (
            <span className="badge pending">
              {pendingAppointments.length} waiting
            </span>
          )}
        </div>
        <p className="nurse-hint">
          Approving an appointment assigns that mother to you (one patient, one
          nurse).
        </p>
        {apptMsg && <p className="notice notice-success">{apptMsg}</p>}
        {apptError && <p className="notice notice-error">{apptError}</p>}

        {pendingAppointments.length ? (
          pendingAppointments.map((appt) => {
            const risk = appt.mother_summary?.risk_level;
            const symptoms: string[] = appt.mother_summary?.indicators?.symptoms || [];
            const fetal = appt.mother_summary?.indicators?.fetal_movement;

            return (
              <article
                key={appt.id}
                className={`appt-card${risk ? ` risk-${risk}` : ""}`}
              >
                <div className="appt-card-main">
                  <div className="appt-card-title">
                    <h3 className="appt-mother-name">
                      {appt.mother_name || "Unknown mother"}
                    </h3>
                    {risk && <span className={getBadgeClass(risk)}>{risk}</span>}
                  </div>

                  <dl className="appt-facts">
                    <div className="appt-fact">
                      <dt>Clinic</dt>
                      <dd>{appt.clinic_display || "Unassigned"}</dd>
                    </div>
                    <div className="appt-fact">
                      <dt>When</dt>
                      <dd>{formatDateTime(appt.date_time)}</dd>
                    </div>
                    {appt.mother_summary?.due_date && (
                      <div className="appt-fact">
                        <dt>Due date</dt>
                        <dd>{appt.mother_summary.due_date}</dd>
                      </div>
                    )}
                    {appt.mother_summary?.phone_number && (
                      <div className="appt-fact">
                        <dt>Phone</dt>
                        <dd>{appt.mother_summary.phone_number}</dd>
                      </div>
                    )}
                    {fetal && (
                      <div className="appt-fact">
                        <dt>Fetal movement</dt>
                        <dd>{fetal}</dd>
                      </div>
                    )}
                    {appt.reason && (
                      <div className="appt-fact">
                        <dt>Reason</dt>
                        <dd>{appt.reason}</dd>
                      </div>
                    )}
                  </dl>

                  {symptoms.length > 0 && (
                    <ul className="appt-reasons">
                      {symptoms.map((symptom, index) => (
                        <li key={index}>{symptom.replace(/_/g, " ")}</li>
                      ))}
                    </ul>
                  )}

                  {appt.mother_summary && appt.mother_summary.risk_reasons.length > 0 && (
                    <ul className="appt-reasons">
                      {appt.mother_summary.risk_reasons.map((reason, index) => (
                        <li key={index}>{reason}</li>
                      ))}
                    </ul>
                  )}
                </div>

                <div className="appt-actions">
                  <button
                    onClick={() => handleApprove(appt.id)}
                    disabled={busyApptId === appt.id}
                    className="btn btn-ok"
                  >
                    {busyApptId === appt.id ? "Saving..." : "Approve"}
                  </button>
                  <button
                    onClick={() => handleReject(appt.id)}
                    disabled={busyApptId === appt.id}
                    className="btn btn-danger"
                  >
                    {busyApptId === appt.id ? "Saving..." : "Reject"}
                  </button>
                </div>
              </article>
            );
          })
        ) : (
          <p className="notice notice-empty">
            No pending appointments for your clinic.
          </p>
        )}
      </section>

      <section className="nurse-panel panel">
        <div className="nurse-panel-head">
          <div>
            <span className="eyebrow">Monitoring</span>
            <h2>Automated Safety Alerts</h2>
          </div>
          {highRiskMothers.length > 0 && (
            <span className="badge high">{highRiskMothers.length} flagged</span>
          )}
        </div>

        {highRiskMothers.length ? (
          highRiskMothers.map((mother) => (
            <article key={mother.id} className="alert-card">
              <div className="alert-title">
                <strong>
                  {mother.user.first_name} {mother.user.last_name}
                </strong>
                <span className={getBadgeClass(mother.risk_level)}>
                  {mother.risk_level}
                </span>
              </div>
              <p className="alert-clinic">
                {mother.clinic_name || "Unassigned clinic"}
              </p>
              <ul className="alert-reasons">
                {mother.risk_reasons.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </article>
          ))
        ) : (
          <p className="notice notice-empty">
            No active high-risk alerts right now.
          </p>
        )}
      </section>

      <section className="nurse-panel panel">
        <div className="nurse-panel-head">
          <div>
            <span className="eyebrow">Caseload</span>
            <h2>Assigned Patients</h2>
          </div>
          {mothers.length > 0 && <span className="badge neutral">{mothers.length} total</span>}
        </div>

        {mothers.length ? (
          <div className="mother-grid">
            {mothers.map((mother) => (
              <article key={mother.id} className="mother-card">
                <div className="mother-card-header">
                  <h3>
                    {mother.user.first_name} {mother.user.last_name}
                  </h3>
                  <span className={getBadgeClass(mother.risk_level)}>
                    {mother.risk_level}
                  </span>
                </div>

                <dl className="mother-card-facts">
                  <div>
                    <dt>Clinic</dt>
                    <dd>{mother.clinic_name || "Not assigned"}</dd>
                  </div>
                  <div>
                    <dt>Due</dt>
                    <dd>{mother.due_date || "Unknown"}</dd>
                  </div>
                  <div>
                    <dt>Phone</dt>
                    <dd>{mother.phone_number || "Unknown"}</dd>
                  </div>
                </dl>

                {Object.keys(mother.health_info || {}).length > 0 && (
                  <>
                    <p className="health-info-label">Latest indicators</p>
                    <div className="health-info-grid">
                      {Object.entries(mother.health_info || {}).map(
                        ([key, value]) => (
                          <div key={key} className="health-info-item">
                            <span className="health-info-key">
                              {key.replace(/_/g, " ")}
                            </span>
                            <strong>{String(value)}</strong>
                          </div>
                        )
                      )}
                    </div>
                  </>
                )}
              </article>
            ))}
          </div>
        ) : (
          <p className="notice notice-empty">
            No patients assigned to you yet. Approve a pending appointment to
            take on a patient.
          </p>
        )}
      </section>

      <section className="nurse-panel panel">
        <div className="nurse-panel-head">
          <div>
            <span className="eyebrow">Directory</span>
            <h2>Hospital Network</h2>
          </div>
          {clinics.length > 0 && <span className="badge neutral">{clinics.length} hospitals</span>}
        </div>

        {clinics.length ? (
          <div className="hospital-grid">
            {clinics.map((clinic) => (
              <article key={clinic.id} className="hospital-card">
                <h3>{clinic.name}</h3>
                {clinic.address && <p>{clinic.address}</p>}
                {clinic.phone_number && (
                  <p className="hospital-phone">{clinic.phone_number}</p>
                )}
              </article>
            ))}
          </div>
        ) : (
          <p className="notice notice-empty">No hospitals available yet.</p>
        )}
      </section>
    </div>
  );
};

export default NurseDashboard;
