import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, user, loading, error } = useAuth();
  const [localError, setLocalError] = useState('');

  useEffect(() => {
    console.log('Login useEffect - user mudou:', user); // Debug
    if (user) {
      console.log('Usuário autenticado, redirecionando...'); // Debug
      // Redireciona para dashboard após login bem-sucedido
      window.location.reload();
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError('');
    console.log('Iniciando login...'); // Debug
    try {
      await login(email, password);
      console.log('Login bem-sucedido, aguardando redirecionamento...'); // Debug
      // O redirecionamento será feito pelo useEffect quando user for atualizado
    } catch (err) {
      console.error('Erro no login:', err); // Debug
      setLocalError('Erro ao fazer login');
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <form onSubmit={handleSubmit} style={{ background: '#fff', padding: 32, borderRadius: 16, boxShadow: '0 4px 24px rgba(0,0,0,0.08)', minWidth: 320, maxWidth: 360, width: '100%' }}>
        <h2 style={{ color: '#222', marginBottom: 24, textAlign: 'center' }}>Login</h2>
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 4, color: '#222' }}>E-mail</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%', padding: 10, borderRadius: 8, border: '1px solid #ccc', fontSize: 16 }} />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 4, color: '#222' }}>Senha</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: '100%', padding: 10, borderRadius: 8, border: '1px solid #ccc', fontSize: 16 }} />
        </div>
        {(error || localError) && <div style={{ color: '#d32f2f', marginBottom: 12, textAlign: 'center' }}>{error || localError}</div>}
        <button type="submit" disabled={loading} style={{ width: '100%', padding: 12, borderRadius: 8, background: 'linear-gradient(90deg, #7b6cf6 0%, #5f9df7 100%)', color: '#fff', fontWeight: 600, fontSize: 16, border: 'none', cursor: 'pointer', boxShadow: '0 2px 8px rgba(91, 108, 246, 0.08)' }}>
          {loading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>
    </div>
  );
} 