import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import axios from 'axios';

const EXPO_PUBLIC_BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;
const API_URL = `${EXPO_PUBLIC_BACKEND_URL}/api`;

interface User {
  id: string;
  email: string;
  mobile: string;
  name: string;
  role: string;
  company_id?: string;
  company_name?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (login: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  isLoading: boolean;
}

interface RegisterData {
  email: string;
  mobile: string;
  password: string;
  name: string;
  role: string;
  company_name?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadStoredAuth();
  }, []);

  const loadStoredAuth = async () => {
    try {
      const storedToken = await SecureStore.getItemAsync('auth_token');
      const storedUser = await SecureStore.getItemAsync('user_data');
      
      if (storedToken && storedUser) {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      }
    } catch (error) {
      console.error('Error loading auth:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (login: string, password: string) => {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        login,
        password,
      });

      const { access_token, user: userData } = response.data;
      
      await SecureStore.setItemAsync('auth_token', access_token);
      await SecureStore.setItemAsync('user_data', JSON.stringify(userData));
      
      setToken(access_token);
      setUser(userData);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const register = async (data: RegisterData) => {
    try {
      const response = await axios.post(`${API_URL}/auth/register`, data);

      const { access_token, user: userData } = response.data;
      
      await SecureStore.setItemAsync('auth_token', access_token);
      await SecureStore.setItemAsync('user_data', JSON.stringify(userData));
      
      setToken(access_token);
      setUser(userData);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  };

  const logout = async () => {
    try {
      await SecureStore.deleteItemAsync('auth_token');
      await SecureStore.deleteItemAsync('user_data');
      setToken(null);
      setUser(null);
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, isLoading }}>
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
