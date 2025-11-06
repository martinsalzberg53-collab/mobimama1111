import React, { useState, useEffect } from "react";
import { useUser } from "../context/UserContext"; // 1. Import your hook
import "../styles/MotherDashboard.css";

const AITipsCard = () => {
  // 2. Get the *entire user object* from your context
  const { user } = useUser(); 

  const [allTips, setAllTips] = useState([]);
  const [currentTip, setCurrentTip] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const getNewTip = () => {
    if (allTips.length === 0) return;
    let newTip = currentTip;
    while (newTip === currentTip && allTips.length > 1) {
      newTip = allTips[Math.floor(Math.random() * allTips.length)];
    }
    setCurrentTip(newTip);
  };

  useEffect(() => {
    // 3. Get the token *from* the user object
    const token = user?.token;

    const fetchTips = async () => {
      if (!token) { // Check if the token exists
        setError("You are not logged in.");
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch("/api/tips/tips", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            // 4. Use the token here
            "Authorization": `Bearer ${token}` 
          },
        });

        if (!response.ok) {
          throw new Error("Could not fetch tips. Please try again later.");
        }

        const data = await response.json();

        if (data && data.length > 0) {
          setAllTips(data);
          const randomTip = data[Math.floor(Math.random() * data.length)];
          setCurrentTip(randomTip);
        } else {
          setError("No health tips found.");
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    // Only run fetchTips if we have a user and a token
    if (user && user.token) {
      fetchTips();
    } else {
      // Handle case where user is logged out or data is loading
      setIsLoading(false);
      setError("Please log in to see tips.");
    }
  
  // 5. Re-run this effect if the 'user' object changes (e.g., login/logout)
  }, [user]); 

  // --- Render Logic (stays the same) ---
  const renderContent = () => {
    if (isLoading) {
      return <p>Loading tip...</p>;
    }
    if (error) {
      return <p className="tip-error">{error}</p>;
    }
    if (currentTip) {
      return (
        <>
          <h3>{currentTip.title}</h3>
          <p className="tip-text">"{currentTip.content}"</p>
        </>
      );
    }
    return <p>No tips available right now.</p>;
  };

  return (
    <section className="dashboard-card ai-tips-card">
      <h2>Mobi's Health Tip</h2>
      <div className="tip-content">
        {renderContent()}
      </div>
      <button 
        onClick={getNewTip} 
        className="new-tip-btn" 
        disabled={isLoading || allTips.length < 2}
      >
        Get New Tip
      </button>
    </section>
  );
};

export default AITipsCard;