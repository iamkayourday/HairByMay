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

  // Redirect logged-in users based on their role
  useEffect(() => {
    const token = Cookies.get("accessToken");
    const user = Cookies.get("user") ? JSON.parse(Cookies.get("user")) : null;

    if (token) {
      user?.is_superuser ? navigate("/admin-dashboard") : navigate("/profile");
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        "http://localhost:8000/api/accounts/login/",
        { username, password },
        { headers: { "Content-Type": "application/json" } }
      );

      const userData = response.data.user;

      // Store tokens securely
      Cookies.set("accessToken", response.data.access, {
        expires: 1, secure: process.env.NODE_ENV === "production", sameSite: "strict", path: "/",
      });
      Cookies.set("refreshToken", response.data.refresh, {
        expires: 7, secure: process.env.NODE_ENV === "production", sameSite: "strict", path: "/",
      });
      Cookies.set("user", JSON.stringify(userData), { expires: 1, path: "/" }); // ✅ Store user data

      // Redirect based on user role
      userData.is_superuser ? navigate("/admin-dashboard") : navigate("/profile");
    } catch (error) {
      console.error("Login error:", error);
      setError(error.response?.data?.error || "Invalid credentials");
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

      <div className="forgot-password-link">
        <a href="/password_reset">Forgot password?</a>
      </div>
    </div>
  );
};

export default Login;
