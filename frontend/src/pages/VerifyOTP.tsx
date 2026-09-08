import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import API from "../api/axios";
import "../styles/Register.css";

const VerifyOTP = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { login } = useUser();

  const emailFromState = (location.state as { email?: string })?.email || "";
  const [email, setEmail] = useState(emailFromState);
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [secondsLeft, setSecondsLeft] = useState(7 * 60); // 7 minutes in seconds
  const [canResend, setCanResend] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsLeft((prev) => {
        const next = prev - 1;
        if (next <= 0) {
          clearInterval(timer);
          setCanResend(true);
          return 0;
        }
        return next;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (totalSeconds: number) => {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  };

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const res = await API.post("/users/verify-otp/", {
        email,
        otp,
      });

      if (res.data.token) {
        login(res.data.user, res.data.token);
        setSuccess("Email verified successfully!");
        setTimeout(() => {
          navigate("/NurseDashboard");
        }, 1500);
      }
    } catch (err: any) {
      console.error(err);
      const msg =
        err.response?.data?.error ||
        err.response?.data?.detail ||
        "Verification failed. Please check your code and try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const res = await API.post("/users/resend-otp/", { email });
      setSuccess(res.data.message || "A new code has been sent to your email.");
      setSecondsLeft(7 * 60);
      setCanResend(false);
      setOtp("");
    } catch (err: any) {
      console.error(err);
      const msg =
        err.response?.data?.error ||
        "Could not resend the code. Please try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <h2>Verify Your Email</h2>
      <p className="verify-subtitle">
        A 6-digit verification code was sent to your student email.
      </p>

      <form onSubmit={handleVerify}>
        <input
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          placeholder="Enter 6-digit code"
          type="text"
          value={otp}
          onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
          required
          maxLength={6}
          inputMode="numeric"
        />

        <p className="verify-timer">
          {canResend ? (
            <span className="verify-expired">Code expired. You can resend now.</span>
          ) : (
            <>
              Code expires in <strong>{formatTime(secondsLeft)}</strong>
            </>
          )}
        </p>

        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}

        <button type="submit" disabled={loading || !email || otp.length !== 6}>
          {loading ? "Verifying..." : "Verify Email"}
        </button>

        {canResend && (
          <button
            type="button"
            className="resend-button"
            onClick={handleResend}
            disabled={loading}
          >
            {loading ? "Sending..." : "Resend Code"}
          </button>
        )}
      </form>
    </div>
  );
};

export default VerifyOTP;
