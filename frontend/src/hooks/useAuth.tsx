import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { login as apiLogin, logout as apiLogout, setupAxiosInterceptors } from '../services/auth';

interface User {
  id: number;
  email: string;
}

interface AuthContextType {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
  error: string;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Função para lidar com token expirado
  const handleTokenExpired = () => {
    console.log('Token expirado, limpando sessão...');
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    
    // Forçar reload da página para ir para login
    window.location.href = '/';
  };

  // Configurar interceptors do axios
  useEffect(() => {
    setupAxiosInterceptors(handleTokenExpired);
  }, []);

  // Carregar dados da sessão do localStorage
  useEffect(() => {
    const storedAccess = localStorage.getItem('access_token');
    const storedRefresh = localStorage.getItem('refresh_token');
    const storedUser = localStorage.getItem('user');
    
    if (storedAccess && storedRefresh && storedUser && storedUser !== 'undefined') {
      try {
        const parsedUser = JSON.parse(storedUser);
        setAccessToken(storedAccess);
        setRefreshToken(storedRefresh);
        setUser(parsedUser);
      } catch (error) {
        console.error('Erro ao parsear dados do usuário:', error);
        // Se o JSON for inválido, limpa o localStorage
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
      }
    }
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError('');
    try {
      const data = await apiLogin(email, password);
      console.log('Resposta da API:', data);
      
      setAccessToken(data.access_token);
      setRefreshToken(data.refresh_token);
      
      // Lidar com diferentes estruturas de resposta da API
      let userData: User;
      if (data.user) {
        // Se a API retorna objeto user completo
        userData = data.user;
      } else if (data.user_id) {
        // Se a API retorna apenas user_id, criar objeto user
        userData = {
          id: data.user_id,
          email: email
        };
      } else {
        throw new Error('Estrutura de resposta da API inválida');
      }
      
      setUser(userData);
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user', JSON.stringify(userData));
      
      console.log('Usuário definido:', userData);
    } catch (err: any) {
      console.error('Erro no login:', err);
      setError(err.response?.data?.message || 'Erro ao fazer login');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Tentar fazer logout no servidor
      await apiLogout();
    } catch (error) {
      console.log('Erro no logout do servidor (pode ser normal):', error);
    } finally {
      // Sempre limpar dados locais
      setAccessToken(null);
      setRefreshToken(null);
      setUser(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      
      // Redirecionar para login
      window.location.href = '/';
    }
  };

  const isAuthenticated = !!user && !!accessToken;

  return (
    <AuthContext.Provider value={{ 
      user, 
      accessToken, 
      refreshToken, 
      login, 
      logout, 
      loading, 
      error,
      isAuthenticated 
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth deve ser usado dentro de AuthProvider');
  return ctx;
} 