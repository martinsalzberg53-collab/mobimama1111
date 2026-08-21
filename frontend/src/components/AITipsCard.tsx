import React, { useState, useEffect } from "react";
import { useUser } from "../context/UserContext"; // 1. Import your hook
import API from "../api/axios"; // 2. Import your configured Axios instance
import "../styles/MotherDashboard.css";

const AITipsCard = () => {
  // 3. Get both 'user' and 'token' from context
  const { user, token } = useUser(); 

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
    const fetchTips = async () => {
      setIsLoading(true);
      setError(null);
      try {
        // 4. Use the API instance and the correct URL
        // The Auth header is now added AUTOMATICALLY by the Axios interceptor
        const response = await API.get("/tips/tips");

        // 5. Axios automatically parses JSON and puts it in `response.data`
        const data = response.data;

        if (data && data.length > 0) {
          setAllTips(data);
          const randomTip = data[Math.floor(Math.random() * data.length)];
          setCurrentTip(randomTip);
        } else {
          setError("No health tips found.");
        }
      } catch (err: any) {
        // 6. Axios automatically throws an error on 4xx/5xx status
        console.error(err);
        setError(err.message || "Could not fetch tips. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    // 7. Check for 'token' from context, not 'user.token'
    if (user && token) {
      fetchTips();
    } else {
      setIsLoading(false);
      setError("Please log in to see tips.");
    }
  
  // 8. Add 'token' to the dependency array
  }, [user, token]); 

  // --- Render Logic (This part was already perfect) ---
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
        disabled={isLoading || allTips.length < 2 || error}
      >
        Get New Tip
      </button>
    </section>
  );
};

export default AITipsCard;