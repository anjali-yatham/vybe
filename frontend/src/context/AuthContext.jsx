import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);

  // Check localStorage on init
  useEffect(() => {
    const loggedIn = localStorage.getItem('vybe_logged_in') === 'true';
    setIsLoggedIn(loggedIn);
    setLoading(false);
  }, []);

  const login = () => {
    setIsLoggedIn(true);
    localStorage.setItem('vybe_logged_in', 'true');
  };

  const logout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem('vybe_logged_in');
  };

  const value = {
    isLoggedIn,
    loading,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
