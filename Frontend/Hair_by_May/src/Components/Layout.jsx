import React from "react";
import { Outlet } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";

const Layout = () => {
  return (
    <div>
      {/* ✅ Header Component */}
      <Header />

      {/* ✅ Main Content - Routed Components Will Be Rendered Here */}
      <main style={{ padding: "20px" }}>
        <Outlet />
      </main>

      {/* ✅ Footer Component */}
      <Footer />
    </div>
  );
};

export default Layout;