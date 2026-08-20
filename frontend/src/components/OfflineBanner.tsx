import { useState, useEffect } from "react";
import { useLanguage } from "../context/LanguageContext";

export default function OfflineBanner() {
  const [offline, setOffline] = useState(!navigator.onLine);
  const { t } = useLanguage();

  useEffect(() => {
    const handleOnline = () => setOffline(false);
    const handleOffline = () => setOffline(true);
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  if (!offline) return null;

  return (
    <div
      style={{
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        background: "#f59e0b",
        color: "#1f2937",
        padding: "12px 20px",
        textAlign: "center",
        fontWeight: 600,
        fontSize: "0.9rem",
        zIndex: 9999,
        boxShadow: "0 -4px 12px rgba(0,0,0,0.1)",
      }}
    >
      {t("offline.banner")}
    </div>
  );
}
