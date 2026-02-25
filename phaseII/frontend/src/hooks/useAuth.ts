import { useState, useEffect } from 'react';
import { User, LoginResponse } from '@/lib/types';
import { authAPI } from '@/lib/api';
import { atom, useAtom } from 'jotai';
import { authClient } from '@/lib/auth-client';

// Atom for storing user state
export const userAtom = atom<User | null>(null);

export const useAuth = () => {
  const [user, setUser] = useAtom(userAtom);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check if user is logged in on mount
  useEffect(() => {
    const checkSession = async () => {
      try {
        setLoading(true);
        const session = await authClient.getSession();
        if (session) {
          const userData = await authAPI.getMe();
          setUser(userData);
        }
        setError(null);
      } catch (err) {
        console.error('Failed to get session:', err);
        setError('Failed to get session');
        logout();
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);

      const result = await authAPI.login(email, password);

      if (result?.error) {
        setError(result.error.message || 'Login failed');
        setLoading(false);
        return { success: false, error: result.error.message || 'Login failed' };
      }

      // The login response now includes user data directly
      // So we can extract it from the result
      if (result.data && (result.data as LoginResponse).user) {
        setUser((result.data as LoginResponse).user);
      } else {
        // Fallback to fetching user data
        const userData = await authAPI.getMe();
        setUser(userData);
      }

      return { success: true };
    } catch (err: any) {
      console.error('Login failed:', err);
      setError(err.message || 'Login failed');
      setLoading(false);
      return { success: false, error: err.message || 'Login failed' };
    }
  };

  const register = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);

      const result = await authAPI.register(email, password);

      if (result?.error) {
        setError(result.error.message || 'Registration failed');
        setLoading(false);
        return { success: false, error: result.error.message || 'Registration failed' };
      }

      // User is automatically logged in after registration
      // The registration process now logs the user in and sets the token
      // So we can get the user data from the session
      const userData = await authAPI.getMe();
      setUser(userData);

      return { success: true };
    } catch (err: any) {
      console.error('Registration failed:', err);
      setError(err.message || 'Registration failed');
      setLoading(false);
      return { success: false, error: err.message || 'Registration failed' };
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
      setUser(null);
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  return {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user
  };
};