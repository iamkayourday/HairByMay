import React from "react";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

const Logout = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // ✅ Remove tokens from cookies
    Cookies.remove("accessToken");
    Cookies.remove("refreshToken");

    alert("Logged out successfully!");

    // ✅ Navigate back to login page
    navigate("/login");
  };

  return <button onClick={handleLogout}>Logout</button>;
};

export default Logout;