import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./Components/Header";
import Login from "./Auth/Login";
import Register from "./Auth/Register";
import Profile from "./Pages/Profile";
import PasswordResetRequest from "./Auth/PasswordResetRequest";
import PasswordResetConfirm from "./Auth/PasswordResetConfirm";
import PasswordComplete from "./Auth/PasswordComplete";
import Logout from "./Auth/LogOut";
import Services from "./Pages/Services";
import ServiceDetails from "./Pages/ServiceDetails";
import ProtectedRoute from "./Routes/ProtectedRoutes"; // Import from separate file
import AuthRoute from "./Routes/AuthRoutes"; // Import from separate file


const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        {/* Public routes (no auth required) */}
        <Route path="/password_reset" element={<PasswordResetRequest />} />
        <Route path="/reset/:uidb64/:token/" element={<PasswordResetConfirm />} />
        <Route path="/reset/done" element={<PasswordComplete />} />
        <Route path="/services" element={<Services />} />
        <Route path="/services/:id" element={<ServiceDetails />} />

        {/* Auth-only routes (redirect to login if unauthenticated) */}
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/logout" element={<ProtectedRoute><Logout /></ProtectedRoute>} />

        {/* Guest-only routes (redirect to profile if authenticated) */}
        <Route path="/login" element={<AuthRoute><Login /></AuthRoute>} />
        <Route path="/register" element={<AuthRoute><Register /></AuthRoute>} />
      </Routes>
    </Router>
  );
};

export default App;