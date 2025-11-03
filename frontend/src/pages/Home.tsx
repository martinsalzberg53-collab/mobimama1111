import React from "react";
import { Link } from "react-router-dom";
import "../styles/Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <header className="home-hero">
        <h1>Mobi Mama</h1>
        <p>AI-powered maternal care that keeps you and your baby healthy and informed.</p>
        <Link to="/login" className="home-cta">
          Get Started
        </Link>
      </header>

      <section className="home-features">
        <div className="feature">
          <h2>Smart Reminders</h2>
          <p>Never miss an appointment. AI keeps track for you.</p>
        </div>
        <div className="feature">
          <h2>AI Health Insights</h2>
          <p>Receive personalized guidance for every stage of your pregnancy.</p>
        </div>
        <div className="feature">
          <h2>Connect with Nurses</h2>
          <p>Professional support at your fingertips, enhanced by AI.</p>
        </div>
      </section>
    </div>
  );
};

export default Home;
