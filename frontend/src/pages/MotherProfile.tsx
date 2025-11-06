import React from "react";
import { useUser } from "../context/UserContext";
import "../styles/MotherProfile.css"; // We'll use a simplified CSS

const MotherProfile = () => {
  const { user } = useUser(); // Gets the user object from your context

  // If the user isn't loaded yet (e.g., on a page refresh), show a message
  if (!user) {
    return (
      <div className="mother-profile-container">
        <h1>Loading Profile...</h1>
      </div>
    );
  }

  // Combine first and last name for display
  const fullName = `${user.first_name || ""} ${user.last_name || ""}`.trim();

  return (
    <div className="mother-profile-container">
      <div className="profile-header">
        <h1>My Profile</h1>
      </div>

      <div className="profile-card">
        {/* --- Account Section --- */}
        <h3 className="profile-section-header">Account Details</h3>
        <div className="profile-field">
          <span className="label">Email:</span>
          <span className="value">{user.email}</span>
        </div>
        <div className="profile-field">
          <span className="label">Account Type:</span>
          <span className="value">{user.role}</span>
        </div>

        {/* --- Personal Section --- */}
        <h3 className="profile-section-header">Personal Details</h3>
        <div className="profile-field">
          <span className="label">Full Name:</span>
          <span className="value">{fullName || "Not set"}</span>
        </div>

        {/* --- Health Section --- */}
        <h3 className="profile-section-header">Health Details</h3>
        <div className="profile-field">
          <span className="label">Assigned Clinic:</span>
          <span className="value">{user.clinic || "Not assigned"}</span>
        </div>
      </div>
    </div>
  );
};

export default MotherProfile;