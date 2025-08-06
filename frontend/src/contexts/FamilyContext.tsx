import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { getUserFamilies } from '../services/family';

interface Family {
  id: number;
  name: string;
}

interface FamilyContextType {
  families: Family[];
  selectedFamilyId: number | null;
  setSelectedFamilyId: (familyId: number) => void;
  loading: boolean;
  error: string | null;
  refreshFamilies: () => void;
}

const FamilyContext = createContext<FamilyContextType | undefined>(undefined);

interface FamilyProviderProps {
  children: ReactNode;
}

export function FamilyProvider({ children }: FamilyProviderProps) {
  const [families, setFamilies] = useState<Family[]>([]);
  const [selectedFamilyId, setSelectedFamilyId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadFamilies = async () => {
    try {
      setLoading(true);
      setError(null);
      const familiesData = await getUserFamilies();
      setFamilies(familiesData);
      
      // Se não há família selecionada e há famílias disponíveis, seleciona a primeira
      if (!selectedFamilyId && familiesData.length > 0) {
        setSelectedFamilyId(familiesData[0].id);
      }
    } catch (err: any) {
      console.error('Erro ao carregar famílias:', err);
      setError(err.response?.data?.error || 'Erro ao carregar famílias');
    } finally {
      setLoading(false);
    }
  };

  const refreshFamilies = () => {
    loadFamilies();
  };

  useEffect(() => {
    loadFamilies();
  }, []);

  const value: FamilyContextType = {
    families,
    selectedFamilyId,
    setSelectedFamilyId,
    loading,
    error,
    refreshFamilies
  };

  return (
    <FamilyContext.Provider value={value}>
      {children}
    </FamilyContext.Provider>
  );
}

export function useFamily() {
  const context = useContext(FamilyContext);
  if (context === undefined) {
    throw new Error('useFamily must be used within a FamilyProvider');
  }
  return context;
} 