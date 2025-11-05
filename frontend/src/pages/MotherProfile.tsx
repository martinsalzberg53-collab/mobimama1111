import React, { useState, useEffect } from "react";
import { useUser } from "../context/UserContext";
import "../styles/MotherProfile.css"; // We'll update this file next

// Helper function to calculate gestation
const calculateGestation = (dueDate) => {
  if (!dueDate) return "N/A";

  const today = new Date();
  const edd = new Date(dueDate);
  
  // Calculate total days of pregnancy (40 weeks = 280 days)
  const totalDays = 280;
  const startDate = new Date(edd.getTime() - totalDays * 24 * 60 * 60 * 1000);
  
  // Difference in days from start date
  const diffTime = Math.abs(today.getTime() - startDate.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  const weeks = Math.floor(diffDays / 7);
  const days = diffDays % 7;

  return `${weeks} weeks, ${days} days`;
};

const MotherProfile = () => {
  const { user } = useUser(); // Gets base info like email, role
  const [isEditing, setIsEditing] = useState(false);
  
  // We use state to hold the profile data, merging the user hook
  // with more detailed (mocked) profile info.
  const [formData, setFormData] = useState({
    email: "",
    role: "",
    username: "",
    phone: "",
    clinic: "",
    dueDate: "",
  });

  // When the component loads, populate formData from the user context
  // In a real app, you'd fetch this detailed profile from your API
  useEffect(() => {
    setFormData({
      email: user?.email || "",
      role: user?.role || "Mother",
      username: user?.username || "Mama Kena", // Mocked
      phone: user?.phone || "024 123 4567", // Mocked
      clinic: user?.clinic || "Accra Health Clinic", // Mocked
      dueDate: user?.dueDate || "2026-03-15", // Mocked
    });
  }, [user]);

  // Handle changes in the form fields
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Handle saving the profile
  const handleSave = (e) => {
    e.preventDefault();
    console.log("Saving data:", formData);
    // In a real app, you would send `formData` to your API here
    // e.g., await updateUserProfile(formData);
    setIsEditing(false);
  };

  // Handle canceling the edit
  const handleCancel = () => {
    setIsEditing(false);
    // Reset form to original user data
    setFormData({
      email: user?.email || "",
      role: user?.role || "Mother",
      username: user?.username || "Mama Kena",
      phone: user?.phone || "024 123 4567",
      clinic: user?.clinic || "Accra Health Clinic",
      dueDate: user?.dueDate || "2026-03-15",
    });
  };

  return (
    <div className="mother-profile-container">
      <div className="profile-header">
        <h1>My Profile</h1>
        <div className="button-group">
          {isEditing ? (
            <>
              <button onClick={handleSave} className="save-btn">Save</button>
              <button onClick={handleCancel} className="cancel-btn">Cancel</button>
            </>
          ) : (
            <button onClick={() => setIsEditing(true)} className="edit-btn">
              Edit Profile
            </button>
          )}
        </div>
      </div>

      <div className="profile-card">
        {isEditing ? (
          /* --- EDITING MODE (FORM) --- */
          <form onSubmit={handleSave}>
            {/* --- Account Section --- */}
            <h3 className="profile-section-header">Account Details</h3>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input type="email" id="email" name="email" value={formData.email} readOnly />
              <small>Email address cannot be changed.</small>
            </div>
            <div className="form-group">
              <label htmlFor="role">Account Type</label>
              <input type="text" id="role" name="role" value={formData.role} readOnly />
            </div>

            {/* --- Personal Section --- */}
            <h3 className="profile-section-header">Personal Details</h3>
            <div className="form-group">
              <label htmlFor="username">Full Name</label>
              <input type="text" id="username" name="username" value={formData.username} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label htmlFor="phone">Phone Number</label>
              <input type="tel" id="phone" name="phone" value={formData.phone} onChange={handleChange} />
            </div>

            {/* --- Pregnancy Section --- */}
            <h3 className="profile-section-header">Pregnancy Details</h3>
            <div className="form-group">
              <label htmlFor="clinic">Assigned Clinic</label>
              <input type="text" id="clinic" name="clinic" value={formData.clinic} readOnly />
            </div>
            <div className="form-group">
              <label htmlFor="dueDate">Estimated Due Date</label>
              <input type="date" id="dueDate" name="dueDate" value={formData.dueDate} onChange={handleChange} />
            </div>
          </form>
        ) : (
          /* --- VIEW MODE (READ-ONLY) --- */
          <>
            {/* --- Account Section --- */}
            <h3 className="profile-section-header">Account Details</h3>
            <div className="profile-field">
              <span className="label">Email:</span>
              <span className="value">{formData.email}</span>
            </div>
            <div className="profile-field">
              <span className="label">Account Type:</span>
              <span className="value">{formData.role}</span>
            </div>

            {/* --- Personal Section --- */}
            <h3 className="profile-section-header">Personal Details</h3>
            <div className="profile-field">
              <span className="label">Full Name:</span>
              <span className="value">{formData.username}</span>
            </div>
            <div className="profile-field">
              <span className="label">Phone Number:</span>
              <span className="value">{formData.phone}</span>
            </div>

            {/* --- Pregnancy Section --- */}
            <h3 className="profile-section-header">Pregnancy Details</h3>
            <div className="profile-field">
              <span className="label">Assigned Clinic:</span>
              <span className="value">{formData.clinic}</span>
            </div>
            <div className="profile-field">
              <span className="label">Estimated Due Date:</span>
              <span className="value">{formData.dueDate}</span>
            </div>
            <div className="profile-field">
              <span className="label">Gestational Age:</span>
              <span className="value">{calculateGestation(formData.dueDate)}</span>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default MotherProfile;