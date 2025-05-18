import Cookies from "js-cookie";
import { Link } from "react-router-dom";
Link
const Header = () => {
  const isLoggedIn = Cookies.get("accessToken");
  const user = Cookies.get("user") ? JSON.parse(Cookies.get("user")) : null;

  return (
    <header className="bg-blue-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">MyApp</Link>
        <nav>
          <ul className="flex space-x-4">
            {isLoggedIn ? (
              user?.is_superuser ? (
                // ✅ Superuser Links
                <>
                  <li><Link to="/admin-dashboard" className="hover:underline">Admin Dashboard</Link></li>
                  <li><Link to="/manage-users" className="hover:underline">Manage Users</Link></li>
                  <li><Link to="/logout" className="hover:underline">Logout</Link></li>
                </>
              ) : (
                // ✅ Normal User Links
                <>
                  <li><Link to="/profile" className="hover:underline">Profile</Link></li>
                  <li><Link to="/services" className="hover:underline">Services</Link></li>
                  <li><Link to="/logout" className="hover:underline">Logout</Link></li>
                </>
              )
            ) : (
              // ✅ Guest Links (Before Login)
              <>
                <li><Link to="/" className="hover:underline">Home</Link></li>
                <li><Link to="/services" className="hover:underline">Services</Link></li>
                <li><Link to="/login" className="hover:underline">Login</Link></li>
                <li><Link to="/register" className="hover:underline">Register</Link></li>
              </>
            )}
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
