import { useCallback } from 'react';

// Hook personalizado para gerenciar família selecionada no localStorage
export function useFamilyStorage() {
  const STORAGE_KEY = 'family-office-selected-family';
  const STORAGE_VERSION_KEY = 'family-office-storage-version';
  const CURRENT_VERSION = '1.0';

  // Validar e migrar dados se necessário
  const validateStorageVersion = useCallback(() => {
    try {
      const version = localStorage.getItem(STORAGE_VERSION_KEY);
      if (version !== CURRENT_VERSION) {
        // Limpar dados antigos em caso de mudança de versão
        localStorage.removeItem(STORAGE_KEY);
        localStorage.setItem(STORAGE_VERSION_KEY, CURRENT_VERSION);
      }
    } catch (error) {
      console.warn('Erro ao validar versão do localStorage:', error);
    }
  }, []);

  // Carregar família selecionada
  const getSelectedFamily = useCallback((): number | null => {
    try {
      validateStorageVersion();
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const familyId = parseInt(stored, 10);
        return isNaN(familyId) ? null : familyId;
      }
      return null;
    } catch (error) {
      console.warn('Erro ao carregar família do localStorage:', error);
      return null;
    }
  }, [validateStorageVersion]);

  // Salvar família selecionada
  const setSelectedFamily = useCallback((familyId: number | null) => {
    try {
      if (familyId) {
        localStorage.setItem(STORAGE_KEY, familyId.toString());
      } else {
        localStorage.removeItem(STORAGE_KEY);
      }
      
      // Disparar evento customizado para outros componentes
      window.dispatchEvent(new CustomEvent('family-changed', { 
        detail: { familyId } 
      }));
    } catch (error) {
      console.warn('Erro ao salvar família no localStorage:', error);
    }
  }, []);

  // Limpar dados
  const clearSelectedFamily = useCallback(() => {
    try {
      localStorage.removeItem(STORAGE_KEY);
      window.dispatchEvent(new CustomEvent('family-changed', { 
        detail: { familyId: null } 
      }));
    } catch (error) {
      console.warn('Erro ao limpar família do localStorage:', error);
    }
  }, []);

  // Verificar se família existe na lista
  const validateFamilyExists = useCallback((familyId: number, families: Array<{ id: number; name: string }>) => {
    return families.some(family => family.id === familyId);
  }, []);

  return {
    getSelectedFamily,
    setSelectedFamily,
    clearSelectedFamily,
    validateFamilyExists
  };
}