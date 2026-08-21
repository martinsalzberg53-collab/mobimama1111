import { useState } from "react";
import API from "../api/axios";
import "../styles/SymptomTracker.css";

export default function SymptomTracker() {
  const [formData, setFormData] = useState({
    headache: false,
    blurredVision: false,
    swelling: false,
    bleeding: false,
    babyMovement: "Normal",
    fever: false,
    vomiting: false,
  });

  const [riskLevel, setRiskLevel] = useState("");
  const [recommendation, setRecommendation] = useState("");
  const [saveMsg, setSaveMsg] = useState("");
  const [saveError, setSaveError] = useState("");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;

    setFormData({
      ...formData,
      [name]:
        type === "checkbox"
          ? (e.target as HTMLInputElement).checked
          : value,
    });
  };

  const getRiskColor = () => {
    if (riskLevel === "High") return "#dc2626";
    if (riskLevel === "Medium") return "#f59e0b";
    return "#059669";
  };

  const saveToProfile = async (symptoms: string[], fetalMovement: string) => {
    setSaveMsg("");
    setSaveError("");
    try {
      const profileRes = await API.get<{ id: number }[]>("/mothers/profiles/");
      const profile = profileRes.data[0];
      if (!profile) {
        setSaveError("No mother profile found. Please contact support.");
        return;
      }
      await API.patch(`/mothers/profiles/${profile.id}/`, {
        health_info: {
          symptoms,
          fetal_movement: fetalMovement,
          last_updated: new Date().toISOString(),
        },
      });
      setSaveMsg("Saved to your profile and sent to your nurse.");
    } catch (err: any) {
      console.error(err);
      setSaveError(
        err.response?.data?.detail ||
        "Could not save your symptoms. Please try again."
      );
    }
  };

  const analyzeSymptoms = () => {
    let risk = "Low";
    let advice =
      "No major warning signs detected. Continue antenatal visits, rest well, and maintain a healthy diet.";

    // HIGH RISK CONDITIONS
    if (formData.bleeding) {
      risk = "High";
      advice =
        "Bleeding during pregnancy is serious. Go to the nearest hospital immediately.";
    } 
    else if (formData.babyMovement === "No Movement") {
      risk = "High";
      advice =
        "No baby movement detected. Seek emergency medical attention immediately.";
    } 
    else if (formData.headache && formData.blurredVision) {
      risk = "High";
      advice =
        "Headache with blurred vision may indicate pre-eclampsia. Seek urgent care.";
    }

    // MEDIUM RISK CONDITIONS
    else if (formData.babyMovement === "Reduced") {
      risk = "Medium";
      advice =
        "Reduced baby movement should be checked by a healthcare professional soon.";
    } 
    else if (formData.swelling && formData.headache) {
      risk = "Medium";
      advice =
        "Swelling with headache may indicate pregnancy complications. Please visit a clinic.";
    } 
    else if (formData.fever) {
      risk = "Medium";
      advice =
        "Fever during pregnancy should be monitored and treated by a healthcare provider.";
    } 
    else if (formData.vomiting) {
      risk = "Medium";
      advice =
        "Persistent vomiting may cause dehydration. Please consult a healthcare provider.";
    }

    setRiskLevel(risk);
    setRecommendation(advice);

    const symptoms: string[] = [];
    if (formData.headache) symptoms.push("headache");
    if (formData.blurredVision) symptoms.push("blurred_vision");
    if (formData.swelling) symptoms.push("swelling");
    if (formData.bleeding) symptoms.push("bleeding");
    if (formData.fever) symptoms.push("fever");
    if (formData.vomiting) symptoms.push("vomiting");

    saveToProfile(symptoms, formData.babyMovement.toLowerCase());
  };

  return (
    <div className="symptom-tracker-container">
      <h2>Maternal Symptom Tracker</h2>
      <p className="tracker-hint">
        Your answers are saved to your profile so your nurse can see how you
        are feeling.
      </p>

      <h3>Symptoms</h3>

      <label className="symptom-check">
        <input
          type="checkbox"
          name="headache"
          checked={formData.headache}
          onChange={handleChange}
        />
        Headache
      </label>

      <label className="symptom-check">
        <input
          type="checkbox"
          name="blurredVision"
          checked={formData.blurredVision}
          onChange={handleChange}
        />
        Blurred Vision
      </label>

      <label className="symptom-check">
        <input
          type="checkbox"
          name="swelling"
          checked={formData.swelling}
          onChange={handleChange}
        />
        Swelling
      </label>

      <label className="symptom-check">
        <input
          type="checkbox"
          name="bleeding"
          checked={formData.bleeding}
          onChange={handleChange}
        />
        Bleeding
      </label>

      <label className="symptom-check">
        <input
          type="checkbox"
          name="fever"
          checked={formData.fever}
          onChange={handleChange}
        />
        Fever
      </label>

      <label className="symptom-check">
        <input
          type="checkbox"
          name="vomiting"
          checked={formData.vomiting}
          onChange={handleChange}
        />
        Vomiting
      </label>

      <label className="symptom-select-label">
        Baby Movement
        <select
          name="babyMovement"
          value={formData.babyMovement}
          onChange={handleChange}
        >
          <option>Normal</option>
          <option>Reduced</option>
          <option>No Movement</option>
        </select>
      </label>

      <button className="analyze-button" onClick={analyzeSymptoms}>
        Analyze Symptoms
      </button>

      {saveMsg && <p className="tracker-success">{saveMsg}</p>}
      {saveError && <p className="tracker-error">{saveError}</p>}

      {riskLevel && (
        <div
          className="tracker-result"
          style={{ borderColor: getRiskColor() }}
        >
          <h3>AI Risk Analysis</h3>
          <p>
            <strong>Risk Level:</strong>{" "}
            <span style={{ color: getRiskColor(), fontWeight: "bold" }}>
              {riskLevel}
            </span>
          </p>
          <p>
            <strong>Recommendation:</strong> {recommendation}
          </p>
        </div>
      )}
    </div>
  );
}
