import React from "react";
import { useUser } from "../context/UserContext";
import "../styles/MotherProfile.css";

const MotherProfile = () => {
  const { user } = useUser();

  return (
    <div className="profile-page-container">
      <h1>My Profile</h1>

      <div className="profile-card">
        <div className="profile-field">
          <span className="label">Email:</span>
          <span className="value">{user?.email}</span>
        </div>

        <div className="profile-field">
          <span className="label">Account Type:</span>
          <span className="value">{user?.role}</span>
        </div>

        <div className="profile-field">
          <span className="label">Clinic:</span>
          <span className="value">{user?.clinic || "Not assigned"}</span>
        </div>

        {/* Optional: Add Edit button later */}
        {/* <button className="edit-btn">Edit Profile</button> */}
      </div>
    </div>
  );
};

export default MotherProfile;
