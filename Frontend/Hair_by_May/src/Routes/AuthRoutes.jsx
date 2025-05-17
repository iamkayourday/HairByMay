// This prevents logged-in users from accessing login/register pages
// and redirects them to their profile page. It also prevents logged-out users from accessing protected routes.
import React from "react";
import { Navigate } from "react-router-dom";
import Cookies from "js-cookie";

const AuthRoute = ({ children }) => {
  if (Cookies.get("accessToken")) {
    return <Navigate to="/profile" replace />;
  }
  return children;
};

export default AuthRoute;