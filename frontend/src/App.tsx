import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import { FamilyProvider, useFamily } from './contexts/FamilyContext';
import { ToastProvider } from './components/Toast';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Assets from './pages/Assets';
import Transactions from './pages/Transactions';
import RiskAnalysis from './pages/RiskAnalysis';
import Upload from './pages/Upload';
import Profile from './pages/Profile';
import AdminPanel from './pages/AdminPanel';
import Login from './pages/Login';

function AppContent() {
  const { isAuthenticated } = useAuth();
  const { families, selectedFamilyId, setSelectedFamilyId, loading: familiesLoading, error: familiesError } = useFamily();
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

  if (!isAuthenticated) {
    return <Login />;
  }

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
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)'
    }}>
      <Header 
        selectedFamilyId={selectedFamilyId}
        onFamilyChange={setSelectedFamilyId}
        families={families}
        familiesLoading={familiesLoading}
        familiesError={familiesError}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />
      
      <div style={{
        maxWidth: 1400,
        margin: '0 auto',
        padding: '24px',
        background: 'white',
        borderRadius: 16,
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
        border: '1px solid rgba(255,255,255,0.2)',
        backdropFilter: 'blur(10px)',
        marginTop: 24,
        marginBottom: 24
      }}>
        <div style={{ marginTop: 0 }}>
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

function AdminRoute() {
  return <AdminPanel />;
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/admin" element={<AdminRoute />} />
        <Route path="*" element={
          <AuthProvider>
            <FamilyProvider>
              <ToastProvider>
                <AppContent />
              </ToastProvider>
            </FamilyProvider>
          </AuthProvider>
        } />
      </Routes>
    </Router>
  );
}
