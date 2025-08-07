import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { getUserFamilies } from '../services/family';
import { useFamilyStorage } from '../hooks/useFamilyStorage';

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

  // Hook para gerenciar localStorage
  const { getSelectedFamily, setSelectedFamily, validateFamilyExists } = useFamilyStorage();

  const loadFamilies = async () => {
    try {
      setLoading(true);
      setError(null);
      const familiesData = await getUserFamilies();
      setFamilies(familiesData);
      
      // Recuperar família selecionada do localStorage
      const storedFamilyId = getSelectedFamily();
      
      // Verificar se a família salva ainda está disponível
      const isStoredFamilyAvailable = storedFamilyId && validateFamilyExists(storedFamilyId, familiesData);
      
      if (isStoredFamilyAvailable) {
        setSelectedFamilyId(storedFamilyId);
      } else if (familiesData.length > 0) {
        // Se não há família válida salva ou não há família selecionada, seleciona a primeira
        const firstFamilyId = familiesData[0].id;
        setSelectedFamilyId(firstFamilyId);
        setSelectedFamily(firstFamilyId);
      } else {
        // Se não há famílias disponíveis, limpa a seleção
        setSelectedFamilyId(null);
        setSelectedFamily(null);
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

  // Função wrapper para setSelectedFamilyId que também salva no localStorage
  const handleSetSelectedFamilyId = (familyId: number) => {
    setSelectedFamilyId(familyId);
    setSelectedFamily(familyId);
  };

  useEffect(() => {
    loadFamilies();
  }, []);

  const value: FamilyContextType = {
    families,
    selectedFamilyId,
    setSelectedFamilyId: handleSetSelectedFamilyId,
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