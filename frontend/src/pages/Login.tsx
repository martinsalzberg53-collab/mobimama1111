import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import API from "../api/axios"; // Your configured Axios instance
import "../styles/Login.css";

const Login = () => {
  // 1. Get the login function from our upgraded context
  const { login } = useUser();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      // 2. Call our single, custom login endpoint
      const res = await API.post("/users/login/", {
        email: email, // Use 'email', not 'username'
        password: password,
      });

      // 3. The response (res.data) contains BOTH the user and token
      //    No second API call is needed!
      const { user, token } = res.data;

      // 4. Call our context's login function with two arguments
      login(user, token);

      // 5. Redirect based on the role
      if (user.role === "MOTHER") {
        navigate("/MotherDashboard");
      } else if (user.role === "NURSE") {
        navigate("/NurseDashboard");
      } else {
        // Handle other roles or default redirect
        navigate("/");
      }
    } catch (err: any) {
      console.error(err);
      if (err.response && err.response.status === 400) {
        setError("Invalid email or password. Please try again.");
      } else {
        setError("A server error occurred. Please try again later.");
      }
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        {/* 6. Changed label from "Username" to "Email" */}
        <label>Email:</label>
        <input
          type="email" // Use type="email" for better validation
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