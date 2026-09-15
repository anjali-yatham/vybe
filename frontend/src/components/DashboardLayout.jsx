import { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { 
  Ticket, 
  ShoppingCart, 
  Repeat, 
  Store, 
  ShieldCheck, 
  History,
  Menu,
  X,
  LogOut
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navItems = [
    { to: '/dashboard', label: 'My Tickets', icon: Ticket },
    { to: '/dashboard/buy', label: 'Buy Tickets', icon: ShoppingCart },
    { to: '/dashboard/resell', label: 'Resell a Ticket', icon: Repeat },
    { to: '/dashboard/marketplace', label: 'Marketplace', icon: Store },
    { to: '/dashboard/trust-score', label: 'My Trust Score', icon: ShieldCheck },
    { to: '/dashboard/history', label: 'Transaction History', icon: History },
  ];

  return (
    <div className="min-h-screen bg-[#FDF6EC] flex">
      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-0 h-full bg-white shadow-lg transition-all duration-300 z-50 ${
          sidebarOpen ? 'w-64' : 'w-20'
        }`}
      >
        {/* Logo Section */}
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <div className={`flex items-center gap-2 ${!sidebarOpen && 'justify-center'}`}>
              <svg width="28" height="28" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 28L4 4H12L16 12L20 4H28L16 28Z" fill="url(#gradient)" />
                <defs>
                  <linearGradient id="gradient" x1="4" y1="4" x2="28" y2="28" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#9c27b0" />
                    <stop offset="0.5" stopColor="#ff4081" />
                    <stop offset="1" stopColor="#ff6b35" />
                  </linearGradient>
                </defs>
              </svg>
              {sidebarOpen && (
                <>
                  <span className="text-xl font-bold text-[#3B2A24]">VYBE</span>
                  <span className="text-[#F5B942] text-xs">✦</span>
                </>
              )}
            </div>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden text-[#3B2A24] hover:text-[#FF8C42] transition-colors"
            >
              {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="p-4 flex-1 overflow-y-auto">
          <ul className="space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <li key={item.to}>
                  <NavLink
                    to={item.to}
                    end={item.to === '/dashboard'}
                    className={({ isActive }) =>
                      `flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                        isActive
                          ? 'bg-gradient-to-r from-[#FF8C42] to-[#FF6F91] text-white shadow-lg'
                          : 'text-[#3B2A24] hover:bg-[#FFF8F0] hover:text-[#FF8C42]'
                      } ${!sidebarOpen && 'justify-center'}`
                    }
                  >
                    <Icon size={20} />
                    {sidebarOpen && <span className="font-medium">{item.label}</span>}
                  </NavLink>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* User Profile Section */}
        <div className="p-4 border-t border-gray-100">
          {sidebarOpen ? (
            <div className="space-y-3">
              {/* User Info */}
              <div className="flex items-center gap-3 px-2">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#FF8C42] to-[#FF6F91] flex items-center justify-center text-white font-bold">
                  U
                </div>
                <div className="flex-1">
                  <p className="text-sm font-semibold text-[#3B2A24]">User Name</p>
                  <p className="text-xs text-[#3B2A24]/60">user@email.com</p>
                </div>
              </div>
              
              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-2 px-4 py-2 rounded-lg text-[#3B2A24] hover:bg-red-50 hover:text-red-600 transition-all"
              >
                <LogOut size={18} />
                <span className="text-sm font-medium">Logout</span>
              </button>
            </div>
          ) : (
            <button
              onClick={handleLogout}
              className="w-full flex justify-center p-2 rounded-lg text-[#3B2A24] hover:bg-red-50 hover:text-red-600 transition-all"
              title="Logout"
            >
              <LogOut size={20} />
            </button>
          )}
        </div>
      </aside>

      {/* Main Content Area */}
      <main
        className={`flex-1 transition-all duration-300 ${
          sidebarOpen ? 'ml-64' : 'ml-20'
        }`}
      >
        {/* Top Header */}
        <header className="bg-white border-b border-gray-100 px-6 lg:px-8 py-4 sticky top-0 z-40">
          <div className="flex items-center justify-between">
            {/* Mobile Menu Toggle */}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden text-[#3B2A24] hover:text-[#FF8C42] transition-colors"
            >
              <Menu size={24} />
            </button>

            {/* Page Title - Will be customized per page */}
            <h1 className="text-2xl font-bold text-[#3B2A24] hidden lg:block">
              Dashboard
            </h1>

            {/* Trust Score Badge */}
            <div className="flex items-center gap-2 bg-gradient-to-r from-[#FFF8F0] to-[#FFE8E0] px-4 py-2 rounded-full border border-[#FF8C42]/20">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-sm font-semibold text-[#3B2A24]">
                Trust Score: <span className="text-[#FF8C42]">85</span>
              </span>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-6 lg:p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
