import React, { createContext, useContext, useState, useEffect } from 'react';
import { loginUser, registerUser, fetchMe, authService } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const savedUser = localStorage.getItem('agrogen_user');
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      return null;
    }
  });
  const [token, setToken] = useState(() => localStorage.getItem('agrogen_token') || null);
  const [loading, setLoading] = useState(true);

  // Initialize auth state
  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('agrogen_token');
      if (storedToken) {
        try {
          const res = await fetchMe();
          setUser(res.data);
          localStorage.setItem('agrogen_user', JSON.stringify(res.data));
        } catch (error) {
          console.error('Failed to verify token:', error);
          logout();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const loginWithTokenAndUser = (accessToken, userData) => {
    setToken(accessToken);
    setUser(userData);
    localStorage.setItem('agrogen_token', accessToken);
    localStorage.setItem('agrogen_user', JSON.stringify(userData));
  };

  const login = async (email, password) => {
    const res = await loginUser({ email, password });
    const { access_token } = res.data;
    localStorage.setItem('agrogen_token', access_token);
    setToken(access_token);

    // Fetch user details
    const userRes = await fetchMe();
    setUser(userRes.data);
    localStorage.setItem('agrogen_user', JSON.stringify(userRes.data));
    return userRes.data;
  };

  const register = async (userData) => {
    // userData: { full_name, email, phone, password, preferred_lang, role }
    await registerUser(userData);
    // Automatically log in after registration
    return await login(userData.email, userData.password);
  };

  const logout = async () => {
    try {
      await authService.logout();
    } catch (err) {
      console.warn('Logout notice:', err);
    } finally {
      localStorage.removeItem('agrogen_token');
      localStorage.removeItem('agrogen_user');
      setToken(null);
      setUser(null);
    }
  };

  const value = {
    user,
    token,
    loading,
    isLoading: loading,
    isAuthenticated: !!token,
    login,
    loginWithTokenAndUser,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
