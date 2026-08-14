import { useState } from "react";

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

  const analyzeSymptoms = () => {
    let risk = "Low";
    let advice =
      "No major warning signs detected. Continue antenatal visits, rest well, and maintain a healthy diet.";

    // HIGH RISK CONDITIONS
    if (formData.bleeding) {
      risk = "High";
      advice =
        "⚠️ Bleeding during pregnancy is serious. Go to the nearest hospital immediately.";
    } 
    else if (formData.babyMovement === "No Movement") {
      risk = "High";
      advice =
        "⚠️ No baby movement detected. Seek emergency medical attention immediately.";
    } 
    else if (formData.headache && formData.blurredVision) {
      risk = "High";
      advice =
        "⚠️ Headache with blurred vision may indicate pre-eclampsia. Seek urgent care.";
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
  };

  const getRiskColor = () => {
    if (riskLevel === "High") return "red";
    if (riskLevel === "Medium") return "orange";
    return "green";
  };

  return (
    <div style={{ maxWidth: "750px", margin: "30px auto", padding: "20px" }}>
      <h2>🩺 Maternal Symptom Tracker</h2>

      <h3>Symptoms</h3>

      <label>
        <input
          type="checkbox"
          name="headache"
          checked={formData.headache}
          onChange={handleChange}
        />
        Headache
      </label>

      <br />

      <label>
        <input
          type="checkbox"
          name="blurredVision"
          checked={formData.blurredVision}
          onChange={handleChange}
        />
        Blurred Vision
      </label>

      <br />

      <label>
        <input
          type="checkbox"
          name="swelling"
          checked={formData.swelling}
          onChange={handleChange}
        />
        Swelling
      </label>

      <br />

      <label>
        <input
          type="checkbox"
          name="bleeding"
          checked={formData.bleeding}
          onChange={handleChange}
        />
        Bleeding
      </label>

      <br />

      <label>
        <input
          type="checkbox"
          name="fever"
          checked={formData.fever}
          onChange={handleChange}
        />
        Fever
      </label>

      <br />

      <label>
        <input
          type="checkbox"
          name="vomiting"
          checked={formData.vomiting}
          onChange={handleChange}
        />
        Vomiting
      </label>

      <br /><br />

      {/* BABY MOVEMENT */}
      <label>Baby Movement</label>
      <select
        name="babyMovement"
        value={formData.babyMovement}
        onChange={handleChange}
      >
        <option>Normal</option>
        <option>Reduced</option>
        <option>No Movement</option>
      </select>

      <br /><br />

      {/* BUTTON */}
      <button onClick={analyzeSymptoms}>
        Analyze Symptoms
      </button>

      {/* RESULT */}
      {riskLevel && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            borderRadius: "10px",
            background: "#f8f8f8",
            border: `2px solid ${getRiskColor()}`,
          }}
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