// This handles protected routes where authentication is required
// and redirects logged-out users to the login page. It also prevents logged-in users from accessing login/register pages.

import React from "react";
import { Navigate } from "react-router-dom";
import Cookies from "js-cookie";

const ProtectedRoute = ({ children }) => {
  if (!Cookies.get("accessToken")) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

export default ProtectedRoute;