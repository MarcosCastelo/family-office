import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import { FamilyProvider, useFamily } from './contexts/FamilyContext';
import { ToastProvider } from './components/Toast';
import Header from './components/Header';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import Assets from './pages/Assets';
import Transactions from './pages/Transactions';
import RiskAnalysis from './pages/RiskAnalysis';
import Upload from './pages/Upload';
import Profile from './pages/Profile';
import AdminPanel from './pages/AdminPanel';
import Login from './pages/Login';

// Componente para verificar se o usuário é admin
function AdminGuard({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  
  // Verificar se o usuário tem permissão de admin
  const isAdmin = user && user.permissions && (
    user.permissions.includes('admin') || 
    user.permissions.includes('admin_system') || 
    user.permissions.includes('admin_users')
  );
  
  if (!isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return <>{children}</>;
}

// Componente para o painel administrativo
function AdminApp() {
  return (
    <div style={{ minHeight: '100vh', background: '#f8fafc' }}>
      <Header />
      <div style={{ maxWidth: 1400, margin: '0 auto', padding: '24px', marginTop: 24, marginBottom: 24 }}>
        <AdminPanel />
      </div>
    </div>
  );
}

// Componente para a aplicação principal (usuários comuns)
function MainApp() {
  const { selectedFamilyId } = useFamily();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedAssetId, setSelectedAssetId] = useState<number | null>(null);

  // Listen for navigation events from Assets page
  React.useEffect(() => {
    const handleNavigateToTransactions = (event: any) => {
      setSelectedAssetId(event.detail.assetId);
      setActiveTab('transactions');
    };

    window.addEventListener('navigate-to-transactions', handleNavigateToTransactions);
    return () => window.removeEventListener('navigate-to-transactions', handleNavigateToTransactions);
  }, []);

  // Reset selected asset when changing tabs
  React.useEffect(() => {
    if (activeTab !== 'transactions') {
      setSelectedAssetId(null);
    }
  }, [activeTab]);

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'assets':
        return <Assets />;
      case 'transactions':
        return <Transactions selectedAssetId={selectedAssetId} />;
      case 'risk':
        return <RiskAnalysis />;
      case 'upload':
        return <Upload />;
      case 'profile':
        return <Profile />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f8fafc' }}>
      <Header />
      <div style={{ maxWidth: 1400, margin: '0 auto', padding: '24px', marginTop: 24, marginBottom: 24 }}>
        <Navigation activeTab={activeTab} onTabChange={setActiveTab} />
        <div style={{ marginTop: 24 }}>
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

function AppContent() {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return <Login />;
  }

  // Verificar se o usuário é admin
  const isAdmin = user && user.permissions && (
    user.permissions.includes('admin') || 
    user.permissions.includes('admin_system') || 
    user.permissions.includes('admin_users')
  );

  return (
    <Routes>
      {/* Rota para administradores */}
      <Route path="/admin" element={
        <AdminGuard>
          <AdminApp />
        </AdminGuard>
      } />
      
      {/* Rota para usuários comuns */}
      <Route path="/dashboard" element={<MainApp />} />
      <Route path="/assets" element={<MainApp />} />
      <Route path="/transactions" element={<MainApp />} />
      <Route path="/risk" element={<MainApp />} />
      <Route path="/upload" element={<MainApp />} />
      <Route path="/profile" element={<MainApp />} />
      
      {/* Rota padrão - redirecionar baseado no tipo de usuário */}
      <Route path="/" element={
        isAdmin ? <Navigate to="/admin" replace /> : <Navigate to="/dashboard" replace />
      } />
      
      {/* Rota para qualquer caminho não encontrado */}
      <Route path="*" element={
        isAdmin ? <Navigate to="/admin" replace /> : <Navigate to="/dashboard" replace />
      } />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <FamilyProvider>
          <ToastProvider>
            <AppContent />
          </ToastProvider>
        </FamilyProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
