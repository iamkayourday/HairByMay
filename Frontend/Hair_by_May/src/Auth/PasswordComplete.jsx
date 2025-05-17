import React from "react";
import { useNavigate } from "react-router-dom";

const PasswordResetComplete = () => {
  const navigate = useNavigate();

  return (
    <div className="password-reset-complete">
      <h2>Password Reset Complete</h2>
      <p>Your password has been successfully reset.</p>
      <button onClick={() => navigate("/login")}>Return to Login</button>
    </div>
  );
};

export default PasswordResetComplete;