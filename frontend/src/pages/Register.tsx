import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import "../styles/Register.css";

const Register = () => {
  const navigate = useNavigate();

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [role, setRole] = useState<"MOTHER" | "NURSE">("MOTHER");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      await API.post("/users/register/", {
        first_name: firstName,
        last_name: lastName,
        email,
        password,
        password2,
        role,
      });

      setSuccess("Registration successful!");
      setTimeout(() => navigate("/login"), 2000);
    } catch (err: any) {
      console.error(err);

      if (err.response?.data) {
        setError(JSON.stringify(err.response.data));
      } else {
        setError("Registration failed. Please try again.");
      }
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
        />

        <input
          placeholder="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
        />

        <input
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <input
          placeholder="Confirm Password"
          type="password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
        />

        <select
          value={role}
          onChange={(e) => setRole(e.target.value as "MOTHER" | "NURSE")}
        >
          <option value="MOTHER">Mother</option>
          <option value="NURSE">Nurse</option>
        </select>

        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}

        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;