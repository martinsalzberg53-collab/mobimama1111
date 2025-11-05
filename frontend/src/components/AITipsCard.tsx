import React, { useState, useEffect } from "react";
import "../styles/MotherDashboard.css";

// Mock tips (could be fetched from your API)
const MOCK_TIPS = [
  "Drink 8-10 glasses of water daily to stay hydrated.",
  "Remember to take your prenatal vitamins every morning.",
  "Go for a 15-minute walk daily to help with circulation.",
  "Eat foods rich in folate, like spinach and lentils.",
  "Rest on your left side to improve blood flow to the baby.",
  "Practice your breathing exercises for 5 minutes.",
];

const AITipsCard = () => {
  const [currentTip, setCurrentTip] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  // Get a random tip to start
  useEffect(() => {
    const initialTip = MOCK_TIPS[Math.floor(Math.random() * MOCK_TIPS.length)];
    // Simulate a slight delay
    setTimeout(() => {
      setCurrentTip(initialTip);
      setIsLoading(false);
    }, 500);
  }, []);

  const getNewTip = () => {
    let newTip = currentTip;
    // Make sure the new tip isn't the same as the old one
    while (newTip === currentTip) {
      newTip = MOCK_TIPS[Math.floor(Math.random() * MOCK_TIPS.length)];
    }
    setCurrentTip(newTip);
  };

  return (
    <section className="dashboard-card ai-tips-card">
      <h2>Mobi's Health Tip</h2>
      {isLoading ? (
        <p>Loading tip...</p>
      ) : (
        <p className="tip-text">"{currentTip}"</p>
      )}
      <button onClick={getNewTip} className="new-tip-btn" disabled={isLoading}>
        Get New Tip
      </button>
    </section>
  );
};

export default AITipsCard;