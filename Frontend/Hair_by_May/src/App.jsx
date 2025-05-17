import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Cookies from "js-cookie";
import Header from "./Components/Header";
import Login from "./Auth/Login";
import Register from "./Auth/Register";
import Profile from "./Pages/Profile";
import PasswordResetRequest from "./Auth/PasswordResetRequest";
import PasswordResetConfirm from "./Auth/PasswordResetConfirm";
import PasswordComplete from "./Auth/PasswordComplete";
import Logout from "./Auth/LogOut";
// import Post from "./Pages/Post";
const ProtectedRoute = ({ children }) => {
  return Cookies.get("accessToken") ? children : <Navigate to="/login" replace />;
};

const AuthRoute = ({ children }) => {
  return Cookies.get("accessToken") ? <Navigate to="/profile" replace /> : children;
};

const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/password_reset" element={<PasswordResetRequest />} />
        <Route path="/reset/:uidb64/:token/" element={<PasswordResetConfirm />} />
        <Route path="/reset/done" element={<PasswordComplete />} />
        <Route path="/login" element={<AuthRoute><Login /></AuthRoute>} />
        <Route path="/register" element={<AuthRoute><Register /></AuthRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/logout" element={<ProtectedRoute><Logout /></ProtectedRoute>} />
        {/* <Route path="/posts" element={<ProtectedRoute><Post /></ProtectedRoute>} /> */}
      </Routes>
    </Router>
  );
};

export default App;