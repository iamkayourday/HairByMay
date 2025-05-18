import React from "react";
import { Link } from "react-router-dom";
import Cookies from "js-cookie";

const Header = () => {
  // Check if user is logged in (based on access token)
  const isLoggedIn = Cookies.get("accessToken");

  return (
    <header className="bg-blue-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo */}
        <Link to="/" className="text-xl font-bold">
          MyApp
        </Link>

        {/* Navigation Links */}
        <nav>
          <ul className="flex space-x-4">
            {isLoggedIn ? (
              <>
                <li>
                  <Link to="/profile" className="hover:underline">Profile</Link>
                </li>
                <li>
                  <Link to="/services" className="hover:underline">Services</Link>
                </li>
                <li>
                  <Link to="/login" className="hover:underline">Login</Link>
                </li>
              </>
            ) : (
              <>
                <li>
                  <Link to="/" className="hover:underline">Home</Link>
                </li>
                <li>
                  <Link to="/services" className="hover:underline">Services</Link>
                </li>
                <li>
                  <Link to="/login" className="hover:underline">Login</Link>
                </li>
                <li>
                  <Link to="/register" className="hover:underline">Register</Link>
                </li>
              </>
            )}
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;