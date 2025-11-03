import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import API from "../api/axios"; // Axios instance with baseURL pointing to /api
import "../styles/Login.css";

const Login = () => {
  const { login } = useUser();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      // 1️⃣ POST credentials to Django JWT endpoint
      const tokenRes = await API.post("/users/token/", {
        username: email, // or "email" if your backend uses email for login
        password: password,
      });

      const accessToken = tokenRes.data.access;

      // 2️⃣ Fetch current user using JWT
      const userRes = await API.get("/users/current_user/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      // 3️⃣ Save user in context with token
      login({ ...userRes.data, token: accessToken });

      // 4️⃣ Redirect based on role
      if (userRes.data.role === "mother") navigate("/MotherDashboard");
      else if (userRes.data.role === "nurse") navigate("/NurseDashboard");
    } catch (err: any) {
      console.error(err);
      setError("Invalid credentials or server error. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <label>Username:</label>
        <input
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {error && <p className="error">{error}</p>}

        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
