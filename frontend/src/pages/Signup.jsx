import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { useAuth } from '../context/AuthContext';
import MascotGreeting from '../components/MascotGreeting';

export default function Signup() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic password confirmation check
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    // For now, just call login and navigate to dashboard
    // TODO: Add backend validation and user registration
    login();
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen flex flex-col lg:flex-row">
      {/* LEFT SIDE - Form */}
      <div className="w-full lg:w-1/2 bg-[#FFF8F0] flex items-center justify-center p-6 lg:p-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-md"
        >
          {/* Logo */}
          <div className="flex items-center gap-2 mb-8">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 28L4 4H12L16 12L20 4H28L16 28Z" fill="url(#gradient)" />
              <defs>
                <linearGradient id="gradient" x1="4" y1="4" x2="28" y2="28" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#9c27b0" />
                  <stop offset="0.5" stopColor="#ff4081" />
                  <stop offset="1" stopColor="#ff6b35" />
                </linearGradient>
              </defs>
            </svg>
            <span className="text-2xl font-bold text-[#3B2A24] tracking-tight">VYBE</span>
            <span className="text-[#F5B942] text-xs ml-0.5">✦</span>
          </div>

          {/* Heading */}
          <h1 className="text-4xl font-bold text-[#3B2A24] mb-2">
            Create your account
          </h1>
          <p className="text-[#3B2A24]/60 mb-8">
            Join Vybe and start experiencing events
          </p>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Name Input */}
            <motion.div
              whileFocus={{ scale: 1.01 }}
              transition={{ duration: 0.2 }}
            >
              <label htmlFor="name" className="block text-sm font-medium text-[#3B2A24] mb-2">
                Full Name
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 rounded-2xl border-2 border-[#3B2A24]/10 bg-white text-[#3B2A24] placeholder-[#3B2A24]/40 focus:outline-none focus:border-[#FF8C42] focus:ring-4 focus:ring-[#FF8C42]/20 transition-all"
                placeholder="John Doe"
              />
            </motion.div>

            {/* Email Input */}
            <motion.div
              whileFocus={{ scale: 1.01 }}
              transition={{ duration: 0.2 }}
            >
              <label htmlFor="email" className="block text-sm font-medium text-[#3B2A24] mb-2">
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 rounded-2xl border-2 border-[#3B2A24]/10 bg-white text-[#3B2A24] placeholder-[#3B2A24]/40 focus:outline-none focus:border-[#FF8C42] focus:ring-4 focus:ring-[#FF8C42]/20 transition-all"
                placeholder="your.email@example.com"
              />
            </motion.div>

            {/* Password Input */}
            <motion.div
              whileFocus={{ scale: 1.01 }}
              transition={{ duration: 0.2 }}
            >
              <label htmlFor="password" className="block text-sm font-medium text-[#3B2A24] mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 rounded-2xl border-2 border-[#3B2A24]/10 bg-white text-[#3B2A24] placeholder-[#3B2A24]/40 focus:outline-none focus:border-[#FF8C42] focus:ring-4 focus:ring-[#FF8C42]/20 transition-all"
                placeholder="Create a strong password"
              />
            </motion.div>

            {/* Confirm Password Input */}
            <motion.div
              whileFocus={{ scale: 1.01 }}
              transition={{ duration: 0.2 }}
            >
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-[#3B2A24] mb-2">
                Confirm Password
              </label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 rounded-2xl border-2 border-[#3B2A24]/10 bg-white text-[#3B2A24] placeholder-[#3B2A24]/40 focus:outline-none focus:border-[#FF8C42] focus:ring-4 focus:ring-[#FF8C42]/20 transition-all"
                placeholder="Re-enter your password"
              />
            </motion.div>

            {/* Submit Button */}
            <motion.button
              type="submit"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full bg-gradient-to-r from-[#FF8C42] to-[#FF6F91] text-white font-semibold py-4 rounded-full shadow-lg hover:shadow-xl transition-all"
            >
              Create Account
            </motion.button>
          </form>

          {/* Login link */}
          <p className="text-center text-[#3B2A24]/60 mt-6">
            Already have an account?{' '}
            <Link 
              to="/login" 
              className="text-[#FF6F91] font-semibold hover:text-[#FF8C42] transition-colors"
            >
              Log in
            </Link>
          </p>
        </motion.div>
      </div>

      {/* RIGHT SIDE - Mascot Greeting */}
      <div className="w-full lg:w-1/2 h-64 lg:h-screen">
        <MascotGreeting />
      </div>
    </div>
  );
}
