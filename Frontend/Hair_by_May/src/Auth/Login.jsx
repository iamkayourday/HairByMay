import React, { useState, useEffect } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Check for existing token and redirect if logged in
  useEffect(() => {
    const token = Cookies.get("accessToken");
    if (token) {
      navigate("/profile");
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent default form submission
    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        "http://localhost:8000/api/accounts/login/",
        { username, password },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      // Store tokens securely
      Cookies.set("accessToken", response.data.access, {
        expires: 1, // 1 day (adjust as needed)
        secure: process.env.NODE_ENV === "production",
        sameSite: "strict",
        path: "/",
      });

      Cookies.set("refreshToken", response.data.refresh, {
        expires: 7, // 7 days
        secure: process.env.NODE_ENV === "production",
        sameSite: "strict",
        path: "/",
      });

      // Optional: Store in localStorage for quick access
      // localStorage.setItem("accessToken", response.data.access);

      // Redirect to protected route
      navigate("/profile");
    } catch (error) {
      console.error("Login error:", error);
      
      if (error.response) {
        setError(
          error.response.data.error ||
          error.response.data.detail ||
          "Invalid credentials"
        );
      } else if (error.request) {
        setError("No response from server");
      } else {
        setError("Login failed: " + error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h1>Login</h1>
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>

      <div className="login-container">
    {error && <div className="error-message">{error}</div>}
    
    
      
      <div className="forgot-password-link">
        <a href="/password_reset">Forgot password?</a>
      </div>
   
  </div>
    </div>
  );
};

export default Login;