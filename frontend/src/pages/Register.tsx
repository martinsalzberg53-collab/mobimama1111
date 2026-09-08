import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import API from "../api/axios";
import "../styles/Register.css";

type Clinic = {
  id: number;
  name: string;
};

const Register = () => {
  const navigate = useNavigate();
  const { logout } = useUser();

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [role, setRole] = useState<"MOTHER" | "NURSE">("MOTHER");
  const [nmcPin, setNmcPin] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [hospital, setHospital] = useState("");
  const [clinics, setClinics] = useState<Clinic[]>([]);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchClinics();
  }, []);

  const fetchClinics = async () => {
    try {
      const response = await API.get<Clinic[]>("/clinics/clinics/");
      setClinics(response.data);
    } catch (err) {
      console.error("Failed to load clinics");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const payload: Record<string, string> = {
        first_name: firstName,
        last_name: lastName,
        email,
        password,
        password2,
        role,
      };

      if (role === "NURSE") {
        payload.nmc_pin = nmcPin;
        payload.phone_number = phoneNumber;
        payload.hospital = hospital;
      }

      const res = await API.post("/users/register/", payload);

      if (res.data.requires_verification) {
        setSuccess("Registration successful! Check your email for a verification code.");
        setTimeout(() => {
          navigate("/verify-otp", { state: { email: res.data.email } });
        }, 1500);
      } else {
        setSuccess("Registration successful!");
        setTimeout(() => {
          logout();
          navigate("/login");
        }, 1500);
      }
    } catch (err: any) {
      console.error(err);
      if (err.response?.data) {
        const data = err.response.data;
        if (typeof data === "object") {
          const messages = Object.entries(data)
            .map(([key, val]) => {
              const text = Array.isArray(val) ? val.join(", ") : String(val);
              return `${text}`;
            })
            .join(" ");
          setError(messages);
        } else {
          setError(String(data));
        }
      } else {
        setError("Registration failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <h2>Register</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          required
        />

        <input
          placeholder="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          required
        />

        <input
          placeholder={role === "NURSE" ? "Official Student Email (e.g., name@school.edu.gh)" : "Email"}
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        {role === "NURSE" && (
          <p className="field-hint">
            Must be an official student/school email address (.edu.gh, .edu, .school)
          </p>
        )}

        <input
          placeholder="Password (min 8 characters)"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
        />

        <input
          placeholder="Confirm Password"
          type="password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
          required
        />

        <select
          value={role}
          onChange={(e) => {
            setRole(e.target.value as "MOTHER" | "NURSE");
            setError("");
            setSuccess("");
          }}
        >
          <option value="MOTHER">Mother</option>
          <option value="NURSE">Nurse</option>
        </select>

        {role === "NURSE" && (
          <>
            <input
              placeholder="NMC PIN (e.g., NMC12345)"
              value={nmcPin}
              onChange={(e) => setNmcPin(e.target.value)}
              required
            />
            <p className="field-hint">Nursing and Midwifery Council PIN</p>

            <input
              placeholder="Phone Number (e.g., 0240000000)"
              type="tel"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              required
            />
            <p className="field-hint">Ghana phone number format: 0XX XXX XXXX</p>

            <select
              value={hospital}
              onChange={(e) => setHospital(e.target.value)}
              required
            >
              <option value="">Select your hospital</option>
              {clinics.map((clinic) => (
                <option key={clinic.id} value={clinic.name}>
                  {clinic.name}
                </option>
              ))}
            </select>
            <p className="field-hint">The hospital where you currently work</p>
          </>
        )}

        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "Registering..." : "Register"}
        </button>
      </form>
    </div>
  );
};

export default Register;
