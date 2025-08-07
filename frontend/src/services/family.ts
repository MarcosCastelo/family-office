import axios from 'axios';

const API_URL = 'http://localhost:5000';

export interface Family {
  id: number;
  name: string;
}

export async function getUserFamilies(): Promise<Family[]> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/families`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.data;
}

export interface FamilyBalance {
  cash_balance: number;
  total_invested: number;
  total_patrimony: number;
  percentual_investido: number;
  asset_allocation: Record<string, number>;
}

export interface CashOperation {
  amount: number;
  description?: string;
}

export async function getFamilyBalance(familyId: number): Promise<FamilyBalance> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/families/${familyId}/balance`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.data;
}

export async function addCashToFamily(familyId: number, operation: CashOperation) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.post(`${API_URL}/families/${familyId}/cash/add`, operation, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.data;
}

export async function withdrawCashFromFamily(familyId: number, operation: CashOperation) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.post(`${API_URL}/families/${familyId}/cash/withdraw`, operation, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.data;
}